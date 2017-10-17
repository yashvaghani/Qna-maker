import json
import os
import http.client, urllib.request, urllib.parse, urllib.error, base64


knowledgebaseid = "bb5fa08b-3f70-4453-9da4-879e12657f84"
subscription_key = "285d4c7ef5d4430895df6fb82b8219c8"


def GetMethodStr(methodcode):
    if methodcode == 1 or methodcode == 5:
        return "POST"
    if methodcode == 2:
        return "DELETE"
    if methodcode == 3 or methodcode == 4:
        return "GET"
    if methodcode == 6:
        return "PUT"
    if methodcode == 7 or methodcode == 8 or methodcode == 9:
        return "PATCH"
    raise Exception("invalid methcode")


def GetLQnaPairs(_list, maxnum):
    num = int(input("number of the QnaPairs:"))
    if num > maxnum:
        num = maxnum
    for i in range(num):
        question = input("enter the question:")
        answer = input("enter the answer:")
        _list.append({"answer": answer, "question": question})
        # print(_list) # debug®
    return


def Geturls(_list, maxnum):
    num = int(input("number of the urls:"))
    if num > maxnum:
        num = maxnum
    for i in range(num):
        url = input()
        _list.append(url)
    return


def GetQuestion(body):
    question = input("ask the question:")
    body["question"] = question
    top = int(input("enter the top number:"))
    body["top"] = top
    return


def GetAlterations(stat_str, altera):
    print("how many alterations you want to ", stat_str, ":")
    num = int(input())
    for i in range(num):
        print("enter the word:")
        word = input()
        altera_words = []
        print("enter some alterations:\nend with char \'0\'")
        altera_word = input()
        while altera_word != '0':
            altera_words.append(altera_word)
            altera_word = input()
        altera.append({"word": word, "alterations": altera_words})
    return


def GetBody(methodcode, body):
    if methodcode == 1:
        qna_name = input("enter the name:")
        body["name"] = qna_name
        qnapairs = []
        GetLQnaPairs(qnapairs, 1000)
        urls = []
        Geturls(urls, 5)
        body["qnaPairs"] = qnapairs
        body["urls"] = urls
        return
    if methodcode == 2:
        return
    if methodcode == 3:
        return
    if methodcode == 4:
        return
    if methodcode == 5:
        GetQuestion(body)
        return
    if methodcode == 6:
        return
    if methodcode == 7:
        train_info = {}
        userid = input("enter the user id:")
        train_info["userID"] = userid
        userquestion = input("enter uesr's question:")
        kbquestion = input("kbquestion ==:")
        kbanswer = input("kbanswer ==:")
        train_info["userQuestion"] = userquestion
        train_info["kbQuestion"] = kbquestion
        train_info["kbAnswer"] = kbanswer
        body["feedbackRecords"] = [train_info]
        return
    if methodcode == 8:
        print("add alterations:")
        alteras = []
        GetAlterations("add", alteras)
        body["add"] = alteras
        alteras = []
        GetAlterations("delete", alteras)
        body["delete"] = alteras
        return
    if methodcode == 9:
        print("add qnapairs:")
        qnapairs = []
        GetLQnaPairs(qnapairs, 100)
        urls = []
        Geturls(urls, 100)
        body["add"] = {"qnaPairs": qnapairs, "urls": urls}
        print("delete qnapairs:")
        qnapairs = []
        GetLQnaPairs(qnapairs, 4)
        urls = []
        Geturls(urls, 4)
        body["delete"] = {"qnapairs": qnapairs, "urls": urls}
        return


def GetDetailUrl(methodcode):
    if methodcode == 3:
        return "/qnamaker/v2.0/knowledgebases/" + knowledgebaseid + "/downloadAlterations"
    if methodcode == 5:
        return "/qnamaker/v2.0/knowledgebases/" + knowledgebaseid + "/generateAnswer"
    if methodcode == 6:
        return "/qnamaker/v2.0/knowledgebases/" + knowledgebaseid
    if methodcode == 7:
        return "/qnamaker/v2.0/knowledgebases/" + knowledgebaseid + "/train"
    if methodcode == 8:
        return "/qnamaker/v2.0/knowledgebases/" + knowledgebaseid + "/updateAlterations"
    if methodcode == 9:
        return "/qnamaker/v2.0/knowledgebases/" + knowledgebaseid


def main():
    print("what do you want?")
    print("1 Create knowledgebase\n2 delete knowledgebase\n3 download alterations")
    print("4 download knowledge base\n5 generate answer\n6 retrain and publish knowledge base")
    print("7 train knowledge base\n8 update alterations\n9 update knowledge base")
    print("Now 3 7 8 is useless")
    methodcode = int(input("enter the method:"))
    try:
        methodstr = GetMethodStr(methodcode)
    except Exception as e:
        print(e)
    headers = {}
    if methodstr != "DELETE" and methodstr != "GET":
        headers["Content-Type"] = "application/json"
    headers["Ocp-Apim-Subscription-Key"] = subscription_key
    body = {}
    GetBody(methodcode, body)
    print("body is:", body)
    # params = urllib.parse.urlencode({})
    try:
        coon = http.client.HTTPSConnection("westus.api.cognitive.microsoft.com")
        detailurl = GetDetailUrl(methodcode)
        coon.request(methodstr, detailurl, json.dumps(body), headers)
        response = coon.getresponse()
        data = response.read()
        # print(type(data))
        data_utf8 = data.decode()
        print(data_utf8)
        if methodcode == 5:
            data_dict = json.loads(data_utf8)
            print("the output answer is:")
            print(data_dict["answers"][0]["answer"])
        coon.close()
    except Exception as e:
        print("Error {0}:{1}".format(e.errno, e.strerror))
    finally:
        print("want to continue?(yes or no)")
        ans = input()
        if ans == "yes":
            main()
        else:
            return


if __name__ == "__main__":
    main()




