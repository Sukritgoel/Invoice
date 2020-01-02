
import re
import datetime

def invoice_extraction(textdata):
                output2=[]
                invoicedate='None'
                for w in textdata:
                        output2.append(w.upper())
                vendor='None'
                try:
                    for x in output2: 
                        if 'LIMITED' in x or 'LTD.' in x or 'LID.' in x or '.LTD' in x or 'CREATIONS' in x  or 'LTD' in x:
                            #print(x)
                            vendor=x
                            break
                except:
                            vendor='None'
                        
                output3=[]
                for x in output2:
                    #print(x)
                    if 'PO DT.' not in x and 'PO DATE:' not in x and 'START DATE:' not in x and 'END DATE:'not  in x:
                #         print(x)
                        output3.append(x)

                dates=[]
                flag=0
                try:
                    for i in output3:        
                        for w in i.split(' '):
                            #if re.match('(\d{2}(/|-|\.)\w{3}(/|-|\.)\d{4})|([a-zA-Z]{3}\s\d{2}(,|-|\.|,)?\s\d{4})|(\d{2}(/|-|\.)\d{2}(/|-|\.)\d+)',w):     
                            #if re.match("^([1-9] |1[0-9]| 2[0-9]|3[0-1])(.|-)([1-9] |1[0-2])(.|-|)20[0-9][0-9]$",w):
                            if re.match("[:]*[0-9]{1,2}[-/.]{1}[0-9]{1,2}[-/.]{1}[0-9]{2,4}$",w):
                                #print(w)
                                dates.append(w)
                                flag=1
                        #dates.sort(key = lambda date: datetime.datetime.strptime(date, '%d/%m/%Y')) 
                            else:
                                if re.match('\d{1,2}\s*[-/.][ADFJEBRPYULGCTVMNOS]\w*[-/.]\d{2,4}', w):
                                    #datetime.datetime.strptime('%s'%(match.group()), "%d-%b-%Y").date().strftime('%d-%b-%Y')
                                    dates.append(w)
                                    flag=2
                        #dates.sort(key = lambda date: datetime.datetime.strptime(date, '%d-%b-%Y')) 
                    
                except Exception as e:
                    print(e)
                    invoicedate='None'
                dateformat=[]
                try:
                    if flag==1:
                        for w in dates:
                            if '.'in w:
                                datetimeobject = datetime.datetime.strptime(w,'%d.%m.%Y')
                                w=datetimeobject.strftime("%d/%m/%Y")
                                dateformat.append(w)
                            else:
                                if '-' in w:
                                    datetimeobject = datetime.datetime.strptime(w,'%d-%m-%Y')
                                    w=datetimeobject.strftime("%d/%m/%Y")
                                    dateformat.append(w)
                                else:
                                    dateformat.append(w)
                except:
                    dateformat=dates
               # print(dateformat)    

                try:
                    if flag==1:
                        for w in dateformat:
                            if  datetime.datetime.strptime(w, '%d/%m/%Y'):
                                dates.sort(key = lambda date: datetime.datetime.strptime(date, '%d/%m/%Y'))
                               
                            invoicedate=dateformat[-1]              


                    else:
                        if flag==2:
                            dates.sort(key = lambda date: datetime.datetime.strptime(date, '%d-%b-%Y'))
                            invoicedate=dates[-1]
                except:
                    invoicedate=dates[0]

                GSTIN=[]
                for i in output2:
                    for w in i.split(' '):
                        if re.match('^[:]*[0-9A-Z]{15}$',w):
                            GSTIN.append(w)

                GSTINno=[]
                print(GSTIN)
                Consigner_GSTINno="None"
                Consignee_GSTINno="None"
                for i in GSTIN:
                    if re.findall('\d',i):
                        GSTINno.append(i)

                try:    
                    if len(GSTINno)>=2:  
                        if len(GSTINno)==2:
                            if GSTINno[0]==GSTINno[1]:
                                Consigner_GSTINno="None"
                                Consignee_GSTINno=GSTINno[1]
                            else:            
                                Consigner_GSTINno=GSTINno[0]
                                Consignee_GSTINno=GSTINno[1]
                        else:
                                Consigner_GSTINno=GSTINno[0]
                                Consignee_GSTINno=GSTINno[1]
                            

                    else:
                        if len(GSTINno)==1:
                                Consigner_GSTINno=GSTINno[0]
                except:
                    
                        Consigner_GSTINno="None"
                        Consignee_GSTINno="None"  

                invoicenum=[]
                for i in output3:
                    for w in i.split(' '):
                        if  re.match('[:]*[0-9]{2}-[0-9]{2}/[A-Z]{4}-[0-9]{3}$',w) or re.match('[:]*[A-Z]{3}/[0-9]{4}-[0-9]{2}/[0-9]{3}$',w) or re.match('[A-Z]{2,3}-[A-Z]{2}-[0-9]{2}$',w) or re.match(':*[A-Z]{2}/[A-Z]{1,3}/[0-9]{3}(/[0-9]{2}-[0-9]{2})*',w) or re.match('[0-9]{3,4}/[0-9]{2,4}-[0-9]{2}',w) :
                            print(w)
                            invoicenum=w
                            break
                        else:
                            if re.match('[:]*[A-Z]{1}-[0-9]{4}$',w) or re.match('[:]*\s*[A-Z]{3,4}[0-9]{8,9}$',w) or re.match('[:]*[0-9]{4}-[0-9]{11}$',w):
                                invoicenum=w
                                break
                                
                            else:
                                if 'INVOICE SERIAL NUMBER' in i or 'INVOICE NO:' in i or 'INVOICE SERIAL NO' in i or 'INVOICE SERIAL NO.' in i or 'INVOICE NO.' in i:
                                    for w in i.split(' '):
                                        #print(w)
                                        if re.findall('\d',w):
                                            invoicenum=w
                                            break     

                invoice=str(invoicenum)
                invoiceno='None'
                for w in invoice.split(' '):
                    if re.findall('\d',w):
                        invoiceno=w    
                invoiceno=invoiceno.replace("]","").replace("'","").replace("[","")
                amount=[]
                # count=0
                numbers = "(ONE|TWO|THREE|FOUR|FIVE|SIX|SEVEN|EIGHT|NINE|TEN|\
                          ELEVEN|TWELVE|THIRTEEN|FOURTEEN|FIFTEEN|SIXTEEN|SEVENTEEN|\
                          EIGHTEEN|NINETEEN|TWENTY|THIRTY|FORTY|FIFTY|SIXTY|SEVENTY|EIGHTY|\
                          NINETY|HUNDRED|THOUSAND|LAKH|LACS|LAC)"
                for i in output2: 
                      # if '(IN WORDS)' in i or 'INWORDS' in i or 'AMOUNT' in i or 'RUPEES':
                            for w in i.split(' '):
                                 if re.match(numbers,w):
                                 #print(w)
                                    amount.append(i)
                                    break

                if len(amount)>=2:
                    if 'ONLY' in amount[0] and amount[1]:
                        Total_amount=amount[1]
                    else:        
                        if 'GRAND' in amount[0] or  'TOTAL' in amount[0] or 'IN WORDS'  in amount[0] or 'RUPEES' in amount[0] or 'INR' in amount[0]:
                              Total_amount=amount[0]+' ' + amount[1]
                        else:
                             Total_amount=amount[1]
                else:
                    if len(amount)==1:
                        Total_amount=amount[0]
                    else:
                        Total_amount="None" 
                    
                                                        
                

                data = {}
                #data = {}
                data['Consigner_GSTINno']=Consigner_GSTINno
                data['Consigner_name'] = vendor
                #data['Consigner_add'] = consigner_address
                data['Consignee_GSTINno']=Consignee_GSTINno
                #data['Consignee_name'] = consignee_name
                #data['Consignee_add']=consignee_address
                data['Invoicedate']=invoicedate
                #data['GSTINum']=GSTINno
                data['Invoiceno']=invoiceno
                data['Total_amount'] = Total_amount
        
                return data

invoice_extraction(['TAX INVOICE (RULE 46)', 'GPC-Veh. Off-RD Ord', 'GSTIN', 'OBAAACH081231ZW', 'GST Inv No :', '3N1912055897', 'Hero MotoCorp Limited', '29.07 2019', 'H', 'Date of Invoice :', '(Global Parte Center )', 'Fin.Doc.No,& Date : 97532602,29.07 2019', 'SP-104 TO 107, NH-8, Delhi Jaipur Highway,', 'Adv.Receipt No :', 'industrial Area, Phase - II.NEEMRANA, District Alwar, RAJASTHAN-301705', 'Pick List No. : 802049694', 'PAN No :', 'AAACHO812J', 'Gross Weight : 1.924', 'No of Cases : 00001', 'Details of Reciever (Billed to)', 'Details of Reciever (Shipped to)', 'Vendor / Customer Code', '30365', 'Vendor / Customer Code 30365', 'Name & Address AKSHA AUTO AGENCY', 'Name & Address AKSHA AUTO AGENCY', 'VIPUL INDL ESTATE SHAPAR VERAVAL', 'VIPUL INDL ESTATE, SHAPAR', 'RAJKOT-360024 MOB: MOB : +918959593131', 'VERAVALRAJKOT-360024', 'State:', 'Gujarat', 'State Code:', 'GJ(24)', 'State: Gujarat', 'State Code: GJ(2', 'GSTN/Unique ID: 24ALNPJ6988Q2ZX', 'Place of Supply: Gujarat', 'GSTN/Unique ID:24ALNPJ6988@2ZX Place of Supply Gujan', 'SriNo', 'Order', 'Material', 'Description', 'HSN', 'CGST SGST', 'IGST', 'MRF', 'Rate', 'No.', 'Code', 'Of Goods', 'Code', '(%)', '(9%)', '(%)', 'Qty.', 'Unit', '(Per Unit)', '(Per Unit)', '5617308', '11200ABG2005', 'CRANK CASE COMP LEFT', '84099192', '28', 'PC', '2,400.00', '1:381 03', 'Mode of Transport. By', 'Safexpress Air', 'Taxable Value', 'Transporter Name', 'SAFEXPRESS PRIVATE LIMITED', 'DIS(5TK) @', '215%', 'Truck No.', 'HRSSAB7240', 'DIS(SLK) @', 'Consignment Note No.', '69600193', 'ADDL DISC.', '0%', 'Fr & Ins@', '2.75%', 'Spl. Freight @', '7%', 'Gross Taxable Value', 'GST Amount', 'Total Invoice Value (In Words)', 'CGST Amount', 'RS. ONE THOUSAND NINE HUNDRED NINETY-TWO AND THIRTY-TWO PAISE ONLY.', 'SGST Amount', 'Total Tax Amount', 'Permit No. :', 'Invoice Amount', 'Now 1 Subject to Deini Jurisdiction Only', 'for Hero MotoCorp Ltd.', '2 Consignment insured against Policy No,', '(Global Part Center)', 'Signature valid', 'Digitally signedcy beer', '2412202245304101000 HDFC ERGO 1.6.2019-31.6 2020', 'Name', 'Date 2019 07 2348:24', 'Designation', 'Hagd Office 14, Commindy Carre, Basant Loh, Vanant Vinar, Now Delhi-116057 Tells+ 01.11 20142451,46044160. Fax :+91-11-26143321,20143108, HaroMotoCom.com CIN: 12501 101 1984PLC', 'Transporter Copy', 'Page 1 0'])