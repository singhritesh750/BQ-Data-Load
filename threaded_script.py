

# Python program to illustrate the concept
# of threading
# importing the threading module
import threading
import os
import re
import time
import datetime
import setup_credential
# import helper_script

#Test case for checking the edge-cases
#ACCOUNTS=['8p8HthXV29qy5NmDtA7y6qzxvECxVGU5XGRsWLku1Ckn']

#Prodution-grade
ACCOUNTS=['8p8HthXV29qy5NmDtA7y6qzxvECxVGU5XGRsWLku1Ckn','HWFzm33hjwjHQB24np1bbW6oPy1xo8kGVfBe2cQyYM7E','A5x1aLP7ribPDuRNXcMaTAzwnyn3mFqK5Xewen4Zk3q1','3itU5ME8L6FDqtMiRoUiT1F7PwbkTtHBbW51YWD5jtjm']

#production-grade
#fhanda = os.popen('acc_to_check.txt')
#acc_to_check = fhanda.read()
#ACCOUNTS = (acc_to_check.strip()).split('\n')



class Geeks():
    # def __init__(self):
    #     self.account1 = 'RdkjabsjcbqskjhvcasjbvclBCVJ'
    # def echo_the_string():
    #     print("the value for the hard coded account is:", account1)
    def account_through_loop(account_loop,ind):
        print('accounts in the thread is: ', str(account_loop))
        # while True:
        # fhand15 = open('acc_to_check.txt')
        # OUTPUT = fhand15.readlines()
        # fhand15.close()
        if os.path.exists('list_of_sig'+ str(ind) +'.txt'):
            os.remove('list_of_sig'+ str(ind) +'.txt')

        # for x in OUTPUT:      //decreasing indentation
        setup_credential.mainnet_cred()
        # x = x.strip('\n')
        #if len(OUTPUT.split(',')):


        if not(os.path.exists("last_transac.txt")):
            fhand5 = open("last_transac.txt",'a')
            fhand5.close()

        fhand5 = open("last_transac.txt")
        output2 = fhand5.readlines()
        fhand5.close()

        accountFound = False

        for row in output2:
            print ('something inside the last transac file')
            row = row.strip('\n')
            row = row.split(',')
            if str(account_loop).strip('\n') == row[0]:
                print ('found the exact account', str(account_loop))
                accountFound = True
                pass

        if not accountFound:
            print('could not found the exact account ', str(account_loop))
            FHAND1 = os.popen('solana-ledger-tool bigtable transaction-history -l . '+str(account_loop))
            output3 = FHAND1.readlines()
            FHAND1.close()
            FHAND2 = open('list_of_sig'+ str(ind) +'.txt','w')
            print('check8')
            for detail_ in output3:
                FHAND2.write(detail_)
                print('detail_ variable is :', str(detail_))
            FHAND2.close()
            #print('printing the datail of file'+'list_of_sig'+ str(ind) +'.txt')

            row = str(account_loop) + "," + str(detail_)
            fhand = open("last_transac.txt",'a')
            fhand.write(row)
            fhand.close()

            #print(' last_transac.txt after changes is:')
            #fhand3a = os.popen('cat last_transac.txt')
            #fhand3a.close()
        else:
            print('The Account is Already existing in the last_transaction.txt file')
            fhand5 = open("last_transac.txt")
            output9 = fhand5.readlines()
            fhand5.close()
            for row in output9:
                row = row.strip('\n')
                row = row.split(',')
                if row[0] == str(account_loop):
                    last_txn_recorded = row[1]
                    fhand4 = os.popen('solana-ledger-tool bigtable transaction-history --before ' + last_txn_recorded + ' -l . ' + str(account_loop))
                    time.sleep(10)
                    print('time.sleep(10)')
                    output1 = fhand4.readlines()
                    fhand4.close()
                    if len(output1) > 0:
                        fhand3 = open('list_of_sig'+ str(ind) +'.txt','w')
                        for sig in output1:
                            fhand3.write(sig)
                            print('single sig is :'+str(sig)+ 'for account :'+str(account_loop))
                        fhand3.close()

                        fin = open("last_transac.txt")
                        data = fin.readlines()
                        fin.close()
                        fin = open("last_transac.txt", "w", newline='')
                        for data_strip in data:
                            data_strip = data_strip.replace(last_txn_recorded, output1[-1].strip('\n'))
                            fin.write(data_strip)
                        fin.close()
                    else:
                        if not (os.path.exists('list_of_sig'+ str(ind) +'.txt')):
                            fhand3b = open('list_of_sig'+ str(ind) +'.txt','w')
                            fhand3b.close()
                        break


        file1 = open('list_of_sig'+ str(ind) +'.txt')
        #print(' last_transac.txt after changes is:')
        #fhand3a = os.popen('cat last_transac.txt')
        #fhand3a.close()

        #fhand6 = open('sig_details.json','w')
        file_name= 'sig_details'+str(ind)+'.json'
        #fhand6 = open(file_name,'w')
        fhand6 = open('sig_details'+str(ind)+'.json','w')
        output2 = file1.readlines()
        file1.close()
        for sig2_ in output2:
            fhand5 = os.popen('curl -X POST -H "Content-Type: application/json" -d \'{"jsonrpc":"2.0", "id":1, "method":"getConfirmedTransaction","params":["'+sig2_.strip("\n")+'","json"]}\' https://api.mainnet-beta.solana.com')
            #time.sleep(4)
            output3 = fhand5.readlines()
            fhand5.close()
            for detail_ in output3:
                detail_ = detail_.strip('\n')
                fhand6.write(detail_+'\n')
        fhand6.close()
        #setup_credential.default_cred()

    #uploading the signature file to GCS
    def upload_sig_file_toCS(file_name):
        setup_credential.default_cred()

        #breaking the loop
        #print('breaking the loop')
        fhand5 = os.popen('gsutil cp ./'+ str(file_name) +' gs://testing_eu_location/')
        fhand5.close()
        #setup_credential.default_cred()
        fhand1 = os.popen('pwd')
        output10 = fhand1.readlines()
        fhand1.close()
        output11 = output10[0].strip('\n')
        fhandle3 = os.popen('bq load --autodetect --source_format=NEWLINE_DELIMITED_JSON bigtable4.main_py gs://testing_eu_location/'+ str(file_name) +' ./bq_load.json')
        #fhandle3 = os.popen('bq load --autodetect --source_format=NEWLINE_DELIMITED_JSON bigtable3.main_py gs://testing_eu_location/sig_details.json ./bq_load.json')
        #print('time.sleep(7)')
        time.sleep(5)
        print('time.sleep(5)')
        fhandle3.close()

    #removing the old uploaded file from GCS    
    def remove_old_CSfile(file_name):
        fhand5 = os.popen('gsutil rm gs://testing_eu_location/'+ str(file_name) + '')
        #fhand5 = os.popen('gsutil rm gs://testing_eu_location/sig_details.json')
        fhand5.close()


# accounts = (OUTPUT.strip('\n')).split(",")
# print("accounts items are: ", accounts)
# for index_of_account in range(len(OUTPUT)):
#count = 0
#thread_count = 0


#variable_dict = {'t0':threading.Thread(target=Geeks.account_through_loop, args=(ACCOUNTS[index_of_account],0,)),'t1':threading.Thread(target=Geeks.account_through_loop, args=(ACCOUNTS[index_of_account+1],1,)),'t2':threading.Thread(target=Geeks.account_through_loop, args=(ACCOUNTS[index_of_account+2],2,))}
count = 0
variable_dict = {}
rem_variable_dict = {}
upload_dict = {}
upload_dict1 = {}
rem_upload_dict = {}
rem_upload_dict1 = {}

for index_of_account in range(len(ACCOUNTS)):

    if (3*int(len(ACCOUNTS)/3))-1 < index_of_account and index_of_account <= (len(ACCOUNTS)-1 ):
        remaining_loop = (len(ACCOUNTS)-1 ) - ((3*int(len(ACCOUNTS)/3))-1)
        print('remaining loops count is : ',remaining_loop)

        if remaining_loop == 0 or remaining_loop >= 0 :
            if remaining_loop == 0:
                remaining_loop = 1
                print('remaining_loop is after changing is , ',remaining_loop)


    #starting the function to start generating the sig.details.json file
        for loops1 in range(remaining_loop):
            rem_variable_dict['t'+str(loops1)] = threading.Thread(target=Geeks.account_through_loop, args=(ACCOUNTS[loops1],loops1,))
            print('t+str(loops1%2) is : '+'t'+str(loops1))
            print('\n\nloopnumber in remaining run: ',loops1)
            count=10
            print('the value for the count is : ',count)
        for key1,value1 in rem_variable_dict.items():
            print('thread is : ', key1)
            value1.start()
        for key1,value1 in rem_variable_dict.items():
            value1.join()

    #starting the next function for uploading the generated sig.details.json file to GCS
        for loops2 in range(remaining_loop):
            rem_upload_dict['t'+str(loops2)] = (threading.Thread(target=Geeks.upload_sig_file_toCS, args=('sig_details'+str(loops2)+'.json',)))
        for key2,value2 in rem_upload_dict.items():
            print('thread is : ', key2)
            value2.start()
        for key2,value2 in variable_dict.items():
            value2.join()


    #starting the next function for deleting the uploaded sig.details.json file from GCS
        for loops3 in range(remaining_loop):
            rem_upload_dict1['t'+str(loops3)] = threading.Thread(target=Geeks.remove_old_CSfile, args=('sig_details'+str(loops3)+'.json',))
        for key2,value2 in rem_upload_dict1.items():
            print('thread is : ', key2)
            value2.start()
        for key2,value2 in rem_upload_dict1.items():
            value2.join()

    #for starting the command execution for the first element in the index_of_accounts
    elif (count == 0):
        variable_dict['t'+str(index_of_account)] = threading.Thread(target=Geeks.account_through_loop, args=(ACCOUNTS[index_of_account],index_of_account,))
        print('t+str(index_of_account%2) is : '+'t'+str(index_of_account))
        print('\n\nindex_of_account in first run: ',index_of_account)
        count=1

    else:
        try:
            index_is = index_of_account%3
            print('\n\nindex_is variable is : ',index_is)
            variable_dict['t'+str(index_is)] = threading.Thread(target=Geeks.account_through_loop, args=(ACCOUNTS[index_of_account],index_is,))
            print('\n\nindex_of_account is : ',index_of_account)
    #        for key in variable_dict.items():
    #            key.start()
            count=2
            print('the value for the count is : ',count)
            if index_of_account %2 ==0 or index_of_account == (len(ACCOUNTS)-1):
                for key,value in variable_dict.items():
                    print('thread is : ', key)
                    value.start()
                for key,value in variable_dict.items():
                    value.join()
            count=3
            print('the value for the count is : ',count)
            for i in range(0,3):
                if (count ==3):
                    upload_dict['t'+str(i)] = (threading.Thread(target=Geeks.upload_sig_file_toCS, args=('sig_details'+str(i)+'.json',)))
                    count = 4
                    print('the value for the count is : ',count)
                    pass
                else:
                    try:
                        upload_dict['t'+str(i)] = (threading.Thread(target=Geeks.upload_sig_file_toCS, args=('sig_details'+str(i)+'.json',)))
    #                    for key1 in upload_dict.items():
    #                        key1.start()
                        count=5
                        print('the value for the count is : ',count)
                        if i%2 == 0 or index_of_account == (len(ACCOUNTS)-1):
                            for key1,value1 in upload_dict.items():
                                value1.start()
                            for key,value in upload_dict.items():
                                value.join()
                        count=6
                        print('the value for the count is : ',count)
                        for y in range(3):
                            print('inside for loop')
                            if (count ==6):
                                print('inside if ')
                                print('upload_dict is :',upload_dict)
                                upload_dict1['t'+str(y)] = threading.Thread(target=Geeks.remove_old_CSfile, args=('sig_details'+str(y)+'.json',))
                                print('upload dict1 is ', upload_dict1)
                                count = 7
                                print('the value for the count is : ',count)
                            else:
                                try:
                                    upload_dict1['t'+str(y)] = threading.Thread(target=Geeks.remove_old_CSfile, args=('sig_details'+str(y)+'.json',))
    #                                for key2 in upload_dict.items():
    #                                    key2.start()
                                    count=8
                                    print('the value for the count is : ',count)
                                    if y%2 == 0 or index_of_account == (len(ACCOUNTS)-1):
                                        for key2,value2 in upload_dict1.items():
                                            value2.start()
                                        for key2,value2 in upload_dict1.items():
                                            value.join()
                                        count=9
                                        print('the value for the count is : ',count)
                                except:
                                    print('not running the loop3 anymore at index :',index_of_account)
                    except:
                        print('not running the loop2 anymore at index :',index_of_account)
        except:
            print('not running the loop1 anymore at index :',index_of_account) 

'''
    count+=1
    print('\n\nindex_of_account is : ',index_of_account)
    try:
        #thread_count+=1
        thread_number = 't'+str(count%3)
        print('thread number is : ',thread_number)
        current_thread= thread_number
        current_thread= threading.Thread(target=Geeks.account_through_loop, args=(ACCOUNTS[index_of_account+(count%3)],(count%3),))
        print('starting the thread '+str(count%3))
        current_thread.start()
        thread_count+=1
#            #t1.join()
##            t1.join()
##            print('finishing the first thread 1')
##            file_name= 'sig_details0.json'
##            t1 = threading.Thread(target=Geeks.upload_sig_file_toCS, args=(file_name,0,))
##            t1.start()
##            t1.join()
##            print('finishing the second thread 1')
##            t1 = threading.Thread(target=Geeks.remove_old_CSfile, args=(file_name,))
##            t1.start()
##            t1.join()
##            print('finishing the third thread 1')
    except:
        print('closing the '+str(thread_number)+' thread due to failure to start it',str(index_of_account))
        os.system(' rm sig_details'+str(count%3)+'.json')
        print('running the command : os.system( rm sig_details+str(count%3)+.json)')
#    try:
#        t2 = threading.Thread(target=Geeks.account_through_loop, args=(ACCOUNTS[index_of_account+1],1,))
#        print('starting the thread 2')
#        t2.start()
#            #t2.join()
##            t2.join()
##            print('finishing the first thread 2')
##            t2 = threading.Thread(target=Geeks.upload_sig_file_toCS, args=(file_name,1,))
##            t2.start()
##            t2.join()
##            print('finishing the second thread 2')
##            t2 = threading.Thread(target=Geeks.remove_old_CSfile, args=(file_name,))
##            t2.start()
##            t2.join()
##            print('finishing the third thread 2')
#    except:
#        print('closing the t2 thread due to failure to start it',str(index_of_account+1))
#        os.system(' rm sig_details1.json')
#    try:
#        t3 = threading.Thread(target=Geeks.account_through_loop, args=(ACCOUNTS[index_of_account+2],2,))
#        print('starting the thread 3')
#        t3.start()
#            #t3.join()
##            t3.join()
##            print('finishing the first thread 3')
##            t3 = threading.Thread(target=Geeks.upload_sig_file_toCS, args=(file_name,2,))
##            t3.start()
##            t3.join()
##            print('finishing the second thread 3')
##            t3 = threading.Thread(target=Geeks.remove_old_CSfile, args=(file_name,))
##            t3.start()
##            t3.join()
##            print('finishing the third thread 3')
#    except:
#        print('closing the t3 thread due to failure to start it',str(index_of_account+2))
#        os.system(' rm sig_details2.json')
    if((count%3) == 0 and thread_count == 1):
        t0.join()
        print('finishing the first thread 1')
        t1.join()
        print('finishing the first thread 2')
        t2.join()
        print('finishing the first thread 3')
    else:
        print('\n\nindex_of_account is : ',index_of_account)
        try:
            t4 = threading.Thread(target=Geeks.account_through_loop, args=(ACCOUNTS[index_of_account],0,))
            print('starting the thread 4')
            t4.start()
            t4.join()
            print('finishing the first thread 4')
    try:
        t1 = threading.Thread(target=Geeks.upload_sig_file_toCS, args=('sig_details0.json',))
        t1.start()
        t2 = threading.Thread(target=Geeks.upload_sig_file_toCS, args=('sig_details1.json',))
        t2.start()
        t3 = threading.Thread(target=Geeks.upload_sig_file_toCS, args=('sig_details2.json',))
        t3.start()
        t1.join()
        print('finishing the second thread 1')
        t2.join()
        print('finishing the second thread 2')
        t3.join()
        print('finishing the second thread 3')
    except:
        print('closing the t3 thread due to failure to start it',str(index_of_account+2))
#    t1.join()
#    print('finishing the second thread 1')
    t1 = threading.Thread(target=Geeks.remove_old_CSfile, args=('sig_details0.json',))
    t1.start()
    t2 = threading.Thread(target=Geeks.remove_old_CSfile, args=('sig_details1.json',))
    t2.start()
    t3 = threading.Thread(target=Geeks.remove_old_CSfile, args=('sig_details2.json',))
    t3.start()
    t1.join()
    print('finishing the third thread 1')
    t2.join()
    print('finishing the third thread 2')
    t3.join()
    print('finishing the third thread 3')
    
#    t2.join()
#    print('finishing the first thread 2')
#    t2 = threading.Thread(target=Geeks.upload_sig_file_toCS, args=(file_name,1,))
#    t2.join()
#    print('finishing the second thread 2')
#    t2 = threading.Thread(target=Geeks.remove_old_CSfile, args=(file_name,))
#    t2.join()
#    print('finishing the third thread 2')
##
#    t3.join()
#    print('finishing the first thread 3')
#    t3 = threading.Thread(target=Geeks.upload_sig_file_toCS, args=(file_name,2,))
#    t3.join()
#    print('finishing the second thread 3')
#    t3 = threading.Thread(target=Geeks.remove_old_CSfile, args=(file_name,))
#    t3.join()
#    print('finishing the third thread 3')

print("the accounts in list are over")
print("Done!")

'''


