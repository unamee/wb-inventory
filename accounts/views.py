import datetime
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template import loader
from accounts.forms import StaffForm, AccountForm
from accounts.models import Account, Item
# Create your views here.
from accounts.decorators import unauthenticated_user, admin_only, allowed_users
# Import pagination
from django.core.paginator import Paginator
# Export import file
from tablib import Dataset
import csv
# export pdf file
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
# export pdf file xhtml2pdf
from django.template.loader import get_template
from xhtml2pdf import pisa


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password is incorrect')

    context = {}
    return render(request, 'accounts/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('loginPage')


@login_required(login_url='loginPage')
@admin_only
def home(request):
    return render(request, 'accounts/home.html')


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin'])
def masterStaff(request):
    staff = User.objects.all().order_by('id').values()
    template = loader.get_template('accounts/master/staff.html')
    context = {'staff': staff}
    return HttpResponse(template.render(context, request))
    # return render(request, 'accounts/master/staff.html', context)


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin'])
def createStaff(request):
    form = StaffForm()
    if request.method == 'POST':
        #print('Printing POST:', request.POST)
        form = StaffForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('staff')

    template = loader.get_template('accounts/master/staff_form.html')
    context = {'form': form}
    return HttpResponse(template.render(context, request))


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin'])
def updateStaff(request, pk):
    staff = User.objects.get(id=pk)
    form = StaffForm(instance=staff)

    if request.method == 'POST':
        form = StaffForm(request.POST, instance=staff)
        if form.is_valid():
            form.save()
            return redirect('staff')

    template = loader.get_template('accounts/master/staff_form.html')
    context = {'form': form}
    return HttpResponse(template.render(context, request))


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin'])
def deleteStaff(request, pk):
    staff = User.objects.get(id=pk)
    if request.method == 'POST':
        staff.delete()
        return redirect('staff')
    template = loader.get_template('accounts/master/delete.html')
    context = {'item': staff}
    return HttpResponse(template.render(context, request))


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin'])
def masterAccount(request):
    
    if request.method == 'POST':
        searched = request.POST['searched']
        account = Account.objects.filter(Q(nama__icontains=searched) | Q(deskripsi__icontains=searched))
        context = {'searched' : searched,
                   'accounts' : account}
    else:    
        account = Account.objects.all().order_by('id').values()

    # set up pagination
    p = Paginator(account, 3)
    page = request.GET.get('page')
    accounts = p.get_page(page)
    nums = "a" * accounts.paginator.num_pages

    template = loader.get_template('accounts/master/account.html')
    context = {'account': account,
               'accounts': accounts,
               'nums': nums}
    return HttpResponse(template.render(context, request))

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin'])
def searchAccount(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        account = Account.objects.filter(nama__icontains=searched)
        context = {'searched' : searched,
                   'accounts' : account}
    else:
        test = 'test aja!'
        context = {'searched' : test}
   
    template = loader.get_template('accounts/master/account.html')
    return HttpResponse(template.render(context, request))    


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin'])
def createAccount(request):
    form = AccountForm()
    if request.method == 'POST':
        #print('Printing POST:', request.POST)
        form = AccountForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('account')

    template = loader.get_template('accounts/master/account_form.html')
    context = {'form': form}
    return HttpResponse(template.render(context, request))


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin'])
def updateAccount(request, pk):
    account = Account.objects.get(id=pk)
    form = AccountForm(instance=account)

    if request.method == 'POST':
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            return redirect('account')

    template = loader.get_template('accounts/master/account_form.html')
    context = {'form': form}
    return HttpResponse(template.render(context, request))


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin'])
def deleteAccount(request, pk):
    account = Account.objects.get(id=pk)
    if request.method == 'POST':
        account.delete()
        return redirect('account')
    template = loader.get_template('accounts/master/delete_account.html')
    context = {'item': account}
    return HttpResponse(template.render(context, request))


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin'])
def importAccount(request):
    template = loader.get_template('accounts/master/import_account.html')
    context = {}
    if request.method == 'POST':
        #account_resource = AccountResource()
        dataset = Dataset()
        new_accounts = request.FILES['my_file']
        #template = loader.get_template('accounts/master/import_account.html')
        #context = {}
        if not new_accounts.name.endswith('xlsx'):
            messages.info(request, 'Wrong Format!')
            return HttpResponse(template.render(context, request))

        imported_data = dataset.load(new_accounts.read(), format='xlsx')
        for data in imported_data:
            value = Account(
                nama=data[0],
                deskripsi=data[1],
            )
            value.save()        
    return HttpResponse(template.render(context, request))

#Generate csv file list
@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin'])
def exportAccount(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Account-'+ str(datetime.datetime.now()) + '.csv'
    
    # create  a csv writer
    writer = csv.writer(response)
    
    # designate the model
    accounts = Account.objects.all().order_by('id')
    
    # add column headings to the csv file
    writer.writerow(['ID','Nama', 'Deskripsi', 'Tanggal Created'])
    
    # loop thu and output
    for account in accounts:
        writer.writerow([account.id, account.nama, account.deskripsi, account.date_created])

    return response

#Generate pdf file list
@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin'])
def exportPdf(request):
    # Create Bytestream buffer
    buf = io.BytesIO()
    # Create a canvas
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    # Create a text object
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14) 
    
    #add some lines of text
    lines = [
        "This is line 1",
        "This is line 2",
        "This is line 3",
    ]
    
    # # designate the model
    accounts = Account.objects.all().order_by('id')
    
    # # create blank list
    lines = []
    
    for account in accounts:   
        lines.append(account.nama)
        lines.append(account.deskripsi)
        lines.append("================")        
    
    # loop
    for line in lines:
        textob.textLine(line)
        
    # Finish up
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)
    
    namaFile = 'account'+str(datetime.datetime.now())+'.pdf'
    
    # return
    return FileResponse(buf, as_attachment=True, filename=namaFile)

#Generate pdf file list
@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin'])
def viewPdf(request):
    return render(request, "accounts/pdf/pdf.html")
    # filePdf = "accounts/pdf/pdf.html"
    # pdf=html2pdf(filePdf)
    # return HttpResponse(pdf, content_type="application/pdf")
    
@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin'])
def print_pdf(request):
    template_path = 'accounts/pdf/printpdf.html'
    context = {}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="accounts_report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
       

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin'])
def masterVendor(request):
    context = {}
    return render(request, 'accounts/master/vendor.html')

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin'])
def viewPurchase(request):
    return render(request, "accounts/pdf/purchase.html")

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin'])
def printPurchase(request):
    template_path = 'accounts/pdf/printpdf.html'
    context = {}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="accounts_report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['staff'])
def userPage(request):
    context = {}
    return render(request, 'accounts/user.html', context)

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['staff'])
def purchaseRequest(request):
    context = {}
    return render(request, 'accounts/transaksi/purchaseRequest.html', context)

# @login_required(login_url='loginPage')
# @allowed_users(allowed_roles=['staff'])
# def createPurchase(request):
#     form = PurchaseForm()
#     if request.method == 'POST':
#         #print('Printing POST:', request.POST)
#         form = PurchaseForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('purchase_request')
        
#     template = loader.get_template('accounts/transaksi/purchase_form.html')
#     context = {'form': form}    
#     return HttpResponse(template.render(context, request))

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['staff'])
def createPurchase(request):    
    if request.method == 'POST':
        searched = request.POST['searched']
        item = Item.objects.filter(Q(nama__icontains=searched) | Q(deskripsi__icontains=searched))
        context = {'searched' : searched,
                   'items' : item}
    else:    
        item = Item.objects.all().order_by('id').values()

    # set up pagination
    p = Paginator(item, 3)
    page = request.GET.get('page')
    items = p.get_page(page)
    nums = "a" * items.paginator.num_pages

    template = loader.get_template('accounts/transaksi/purchase_form.html')
    context = {'item': item,
               'items': items,
               'nums': nums}
    return HttpResponse(template.render(context, request))