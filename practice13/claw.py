import datetime
import os

import bs4
import pymysql
import requests
# HTTPS
from fake_useragent import UserAgent
from pydub import AudioSegment
from selenium import webdriver

LISTENING = 1
READING = 2

AudioSegment.converter = "D:\\ffmpeg-20190323-5252d59-win64-static\\bin\\ffmpeg.exe"
AudioSegment.ffmpeg = "D:\\ffmpeg-20190323-5252d59-win64-static\\bin\\ffmpeg.exe"
AudioSegment.ffprobe = "D:\\ffmpeg-20190323-5252d59-win64-static\\bin\\ffmpeg.exe"


def conn():
    return pymysql.connect(host='localhost',
                           user='root',
                           db='toeic_test',
                           charset='utf8',
                           cursorclass=pymysql.cursors.DictCursor)


def main(SOURCE_URL):
    driver = webdriver.Chrome('D:\chromedriver')
    driver.implicitly_wait(5)
    driver.get(SOURCE_URL)
    s = bs4.BeautifulSoup(driver.page_source, 'lxml')
    title = s.select_one('div.panel-heading > h3').text
    title = title.split(':')[1].strip()
    print(title)
    description = s.select_one("div.panel-body > p").text.strip()
    print("description " + description)
    description_1 = s.select_one("div.panel-body").select_one("#testheader").text.strip()
    print("description_1 " + description_1)
    id = insertTopicType(title, description, description_1, topicType)
    print(id)
    if topicType == LISTENING:
        if 'TOEIC_listening_part1' in SOURCE_URL or 'TOEIC_listening_part2' in SOURCE_URL:
            getQuestionType1Or2(driver, s, id, topicType)
        else:
            getQuestionType3or4(driver, id, topicType)
    else:
        if 'TOEIC_reading' in SOURCE_URL or 'TOEIC_reading5_2' in SOURCE_URL or 'TOEIC_reading2' in SOURCE_URL or 'TOEIC_reading6_2' in SOURCE_URL:
            getQuestionType5or6(driver, s, id, topicType, SOURCE_URL)
        else:
            getQuestionType7or8(driver, s, id, topicType, SOURCE_URL)


def getQuestionType7or8(driver, s, idTypeTopic, topicId, SOURCE_URL):
    question = s.select_one('div#extracttoeic7')
    question = question.text.strip()
    idQuestion = insertQuestion(idTypeTopic, topicId, content=question)
    if idQuestion != -1:
        # questionChild = s.select_one('div.panel-body > #centreposition > #col1 > #form1')
        # questionData = {'contain': question}
        questionChild = s.select_one('div#centreposition > span > form')
        # listQuestionChild = []
        getChildQuestionType7or8(topicId, idTypeTopic, idQuestion, SOURCE_URL, driver, questionChild, False)


def getChildQuestionType7or8(topicId, idTypeTopic, idQuestion, SOURCE_URL, driver, data, isLoop):
    content = data.find("div", {"id": "choices"})
    if content:
        if isLoop:
            question = data.contents[21]
        else:
            question = data.contents[1]

        question = question.strip()
        question = question[1:].strip()
        validAnswer = data.select_one('span').attrs['id']
        if question:
            idQuestionChild = insertQuestionChild(idQuestion, question)
            if idQuestionChild != -1:
                getAnswerAndNextQuestion(driver=driver, content=content, topicId=topicId, idTypeTopic=idTypeTopic,
                                         idQuestion=idQuestion, idQuestionChild=idQuestionChild,
                                         validAnswerId=validAnswer,
                                         SOURCE_URL=SOURCE_URL, isReading=True)
    else:
        # questionData['question'] = listQuestionChild
        # listData.append(questionData)
        driver.find_element_by_xpath('//*[@id="choices"]/input[1]').click()
        s = bs4.BeautifulSoup(driver.page_source, 'lxml')
        nextText = s.select_one('div#testfooter > #nextbutton > input').attrs['value']
        if 'Next Questions' in nextText:
            driver.find_element_by_xpath('//*[@id="nextbutton"]').click()
            driver.implicitly_wait(5)
            s = bs4.BeautifulSoup(driver.page_source, 'lxml')
            getQuestionType7or8(driver, s, idTypeTopic, topicId, SOURCE_URL)
        else:
            if SOURCE_URL == 'https://www.examenglish.com/TOEIC/toeic_reading7.htm':
                main("https://www.examenglish.com/TOEIC/toeic_reading7_2.htm")
            elif SOURCE_URL == "https://www.examenglish.com/TOEIC/toeic_reading7_2.htm":
                main("https://www.examenglish.com/TOEIC/toeic_double_passages.htm")
            elif SOURCE_URL == "https://www.examenglish.com/TOEIC/toeic_double_passages.htm":
                main("https://www.examenglish.com/TOEIC/toeic_double_passages_test2.htm")


def getQuestionType5or6(driver, s, idTypeTopic, topicId, SOURCE_URL):
    answerA = {}
    answerB = {}
    answerC = {}
    answerD = {}
    answerCorrect = {}
    s = s.select_one('div#centreposition > span')
    validAnswer = s.select_one('span').attrs['id']
    content = s.text.strip()
    content = content[2:].strip()
    idQuestion = insertQuestion(idTypeTopic, topicId, content=content)
    if idQuestion != -1:
        listAnswer = s.select('form > div > span')
        position = 0
        answer_type = 1
        for index, answer in enumerate(listAnswer):
            position += 1
            if position > 4:
                break
            else:
                id = answer.attrs['id']
                print(id)
                isAnswer = checkAnswerQuestion(driver, validAnswer, id, True)
                print(isAnswer)
                print(answer.text)
                if index == 0:
                    answerA['content'] = answer.text.strip()
                    insertAnswer(idQuestion, answerA['content'])
                if index == 1:
                    if isAnswer:
                        answer_type = 2
                    answerB['content'] = answer.text.strip()
                    insertAnswer(idQuestion, answerB['content'])
                if index == 2:
                    if isAnswer:
                        answer_type = 3
                    answerC['content'] = answer.text.strip()
                    insertAnswer(idQuestion, answerC['content'])
                if index == 3:
                    if isAnswer:
                        answer_type = 4
                    answerD['content'] = answer.text.strip()
                    insertAnswer(idQuestion, answerD['content'])

        if answer_type == 1:
            answerCorrect['content'] = answerA['content']
            insertAnswerQuestion(idQuestion, answerA['content'])
        elif answer_type == 2:
            answerCorrect['content'] = answerB['content']
            insertAnswerQuestion(idQuestion, answerB['content'])
        elif answer_type == 3:
            answerCorrect['content'] = answerC['content']
            insertAnswerQuestion(idQuestion, answerC['content'])
        elif answer_type == 4:
            answerCorrect['content'] = answerD['content']
            insertAnswerQuestion(idQuestion, answerD['content'])

        # listData.append({'content': content, 'answerA': answerA, 'answerB': answerB, 'answerC': answerC, 'answerD': answerD,
        #                  'answerCorrect': answerCorrect})

        # print(listData)
        s = bs4.BeautifulSoup(driver.page_source, 'lxml')
        nextText = s.select_one('div#testfooter > span#nextbutton > input').attrs['value']
        if 'Next' in nextText:
            driver.find_element_by_xpath('//*[@id="nextbutton"]').click()
            driver.implicitly_wait(5)
            s = bs4.BeautifulSoup(driver.page_source, 'lxml')
            getQuestionType5or6(driver, s, idTypeTopic, topicId, SOURCE_URL)
        else:
            if SOURCE_URL == 'https://www.examenglish.com/TOEIC/TOEIC_reading.htm':
                main("https://www.examenglish.com/TOEIC/TOEIC_reading5_2.htm")
            elif SOURCE_URL == "https://www.examenglish.com/TOEIC/TOEIC_reading5_2.htm":
                main("https://www.examenglish.com/TOEIC/TOEIC_reading2.htm")
            elif SOURCE_URL == "https://www.examenglish.com/TOEIC/TOEIC_reading2.htm":
                main("https://www.examenglish.com/TOEIC/TOEIC_reading6_2.htm")
            else:
                main("https://www.examenglish.com/TOEIC/toeic_reading7.htm")


def getQuestionType3or4(driver, idTypeTopic, topicId):
    driver.find_element_by_xpath('//*[@id="jplayer_play"]').click()
    driver.implicitly_wait(5)
    s = bs4.BeautifulSoup(driver.page_source, 'lxml')
    audio = s.select_one('div.panel-body > #jquery_jplayer > #jqjp_audio_0').attrs['src']
    print(audio)
    audio = downloadFile('audio_question', audio, False, True, True, idTypeTopic)
    print("Audio : %s" % audio)
    idQuestion = insertQuestion(idTypeTopic, topicId, audio=audio)
    if idQuestion != -1:
        questionChild = s.select_one('div.panel-body > #centreposition > #col1 > #form1')
        getQuestion(topicId, idTypeTopic, idQuestion, driver, questionChild, False)


def getQuestion(topicId, idTypeTopic, idQuestion, driver, dataContent, isLoop):
    global topicType
    content = dataContent.find("div", {"id": "choices"})
    if content:
        if isLoop:
            question = dataContent.contents[21]
        else:
            question = dataContent.contents[1]
        question = question.strip()
        question = question[1:].strip()
        validAnswer = dataContent.select_one('span').attrs['id']
        if question:
            idQuestionChild = insertQuestionChild(idQuestion, question)
            if idQuestionChild != -1:
                getAnswerAndNextQuestion(topicId=topicId, idTypeTopic=idTypeTopic, idQuestion=idQuestion,
                                         idQuestionChild=idQuestionChild, driver=driver, content=content, validAnswerId=validAnswer)
    else:
        driver.find_element_by_xpath('//*[@id="choices"]/input[1]').click()
        s = bs4.BeautifulSoup(driver.page_source, 'lxml')
        nextText = s.select_one('div.panel-body > #testfooter > #nextbutton > input').attrs['value']
        if 'Next' in nextText:
            driver.find_element_by_xpath('//*[@id="nextbutton"]').click()
            driver.implicitly_wait(5)
            getQuestionType3or4(driver, idTypeTopic, topicId)
        else:
            if idTypeTopic == 3:
                main('https://www.examenglish.com/TOEIC/TOEIC_listening_part4.htm')


def getAnswerAndNextQuestion(driver, content, validAnswerId, topicId=None, idTypeTopic=None, idQuestion=None,
                             idQuestionChild=None, isReading=False, SOURCE_URL=None):
    answer_type = 1
    answerA = {}
    answerB = {}
    answerC = {}
    answerD = {}
    # answerCorrect = {}
    # questionChild = {'question': contentQuestionChild}
    listAnswer = content.select('a.achoice')
    position = 0
    for index, answer in enumerate(listAnswer):
        position += 1
        if position > 4:
            break
        else:
            id = answer.attrs['id']
            # print(id)
            isAnswer = checkAnswerQuestion(driver, validAnswerId, id)
            # print(isAnswer)
            # print(answer.text)
            if index == 0:
                answerA['content'] = answer.text.strip()
                insertAnswer(idQuestion, answerA['content'], questionChildId=idQuestionChild)
            if index == 1:
                if isAnswer:
                    answer_type = 2
                answerB['content'] = answer.text.strip()
                insertAnswer(idQuestion, answerB['content'], questionChildId=idQuestionChild)
            if index == 2:
                if isAnswer:
                    answer_type = 3
                answerC['content'] = answer.text.strip()
                insertAnswer(idQuestion, answerC['content'], questionChildId=idQuestionChild)
            if index == 3:
                if isAnswer:
                    answer_type = 4
                answerD['content'] = answer.text.strip()
                insertAnswer(idQuestion, answerD['content'], questionChildId=idQuestionChild)

    # questionChild['answerA'] = answerA
    # questionChild['answerB'] = answerB
    # questionChild['answerC'] = answerC
    # questionChild['answerD'] = answerD

    # print(answer_type)
    if answer_type == 1:
        insertAnswerQuestion(idQuestion, answerA['content'], idQuestionChild)
    elif answer_type == 2:
        insertAnswerQuestion(idQuestion, answerB['content'], idQuestionChild)
    elif answer_type == 3:
        insertAnswerQuestion(idQuestion, answerC['content'], idQuestionChild)
    elif answer_type == 4:
        insertAnswerQuestion(idQuestion, answerD['content'], idQuestionChild)

    # questionChild['answerCorrect'] = answerCorrect

    if not isReading:
        getQuestion(topicId, idTypeTopic, idQuestion, driver, content, True)
    else:
        getChildQuestionType7or8(topicId, idTypeTopic, idQuestion, SOURCE_URL, driver, content, True)


def checkAnswerQuestion(driver, validAnswerId, id, isReading=False):
    if isReading:
        path = '//*[@id="%s"]/a' % id
    else:
        path = '//*[@id="%s"]' % id
    # print(path)
    driver.find_element_by_xpath(path).click()
    s = bs4.BeautifulSoup(driver.page_source, 'lxml')
    answerQuestion = s.find("span", {"id": validAnswerId}).select_one('img').attrs['alt']
    if 'Correct!' in answerQuestion:
        return True
    return False


def getQuestionType1Or2(driver, s, idTypeTopic, topicId):
    image = ''
    content = ''
    answerA = {}
    answerB = {}
    answerC = {}
    answerD = {}
    if idTypeTopic == 1:
        image = s.select_one('div.panel-body > #centreposition > #image > img').attrs['src']
        print(image)
        image = downloadFile('images', image, True)
        print(image)
    driver.find_element_by_xpath('//*[@id="scriptbutton"]').click()
    s = bs4.BeautifulSoup(driver.page_source, 'lxml')
    scrip = s.select_one('div.panel-body > #centreposition > #script3').contents
    if idTypeTopic == 1:
        answerContentA = str(scrip[1]).split('.')[1].strip()
        answerContentB = str(scrip[3]).split('.')[1].strip()
        answerContentC = str(scrip[5]).split('.')[1].strip()
        answerContentD = str(scrip[7]).split('.')[1].strip()
        answerA['content'] = answerContentA
        answerB['content'] = answerContentB
        answerC['content'] = answerContentC
        answerD['content'] = answerContentD
    elif idTypeTopic == 2:
        content = scrip[1].strip()
        answerContentA = str(scrip[3]).split('.')[1].strip()
        answerContentB = str(scrip[5]).split('.')[1].strip()
        answerContentC = str(scrip[7]).split('.')[1].strip()
        answerA['content'] = answerContentA
        answerB['content'] = answerContentB
        answerC['content'] = answerContentC
        print(content)
    idQuestion = insertQuestion(idTypeTopic, topicId, image, content)
    if idQuestion != -1:
        driver.find_element_by_xpath('//*[@id="jplayer_play"]').click()
        listAudio = []
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        # print("Time - current : %s" % current_time)
        while True:
            try:
                now = datetime.datetime.now()
                time = now.strftime("%H:%M:%S")
                # print("Time - time : %s" % time)
                minusTime = datetime.datetime.strptime(time, "%H:%M:%S") - datetime.datetime.strptime(current_time,
                                                                                                      "%H:%M:%S")
                minusTime = minusTime.total_seconds() / 60.0
                print(minusTime)
                if minusTime > 2:
                    print("break")
                    break
                s = bs4.BeautifulSoup(driver.page_source, 'lxml')
                audio = s.select_one('div.panel-body > #jquery_jplayer > #jqjp_audio_0').attrs['src']
                if not listAudio.__contains__(audio):
                    listAudio.append(audio)
            except Exception as e:
                print(e)
                if listAudio:
                    break
                else:
                    driver.find_element_by_xpath('//*[@id="jplayer_play"]').click()
                    driver.implicitly_wait(1)
        print(listAudio)
        combined_sounds = AudioSegment.empty()
        audioChild = None
        if listAudio:
            del listAudio[0]
            if listAudio:
                audio = downloadFile('audio', listAudio[0], False)
                print(audio)
                if audio:
                    if idTypeTopic == 2:
                        audioChild = audio.split('audio/')[1]
                    combined_sounds = AudioSegment.from_mp3(audio)
                for index, item in enumerate(listAudio):
                    if index == 0:
                        continue
                    audio = downloadFile('audio', item, False)
                    print(audio)
                    if audio:
                        if idTypeTopic == 1:
                            if index == 1:
                                answerA['audio'] = audio.split('audio/')[1]
                            if index == 3:
                                answerB['audio'] = audio.split('audio/')[1]
                            if index == 5:
                                answerC['audio'] = audio.split('audio/')[1]
                            if index == 7:
                                answerD['audio'] = audio.split('audio/')[1]
                        elif idTypeTopic == 2:
                            if index == 2:
                                answerA['audio'] = audio.split('audio/')[1]
                            if index == 4:
                                answerB['audio'] = audio.split('audio/')[1]
                            if index == 6:
                                answerC['audio'] = audio.split('audio/')[1]
                        combined_sounds += AudioSegment.from_mp3(audio)
                dirAudio = 'audio_question'
                if not os.path.isdir('audio_question'):
                    os.mkdir('audio_question')
                audioQuestion = 'audio_question_type' + str(idTypeTopic) + '_id_' + str(idQuestion) + '.mp3'
                if not os.path.exists(dirAudio + '/' + audioQuestion):
                    combined_sounds.export(dirAudio + '/' + audioQuestion, format="mp3")
                updateQuestion(idQuestion, audioQuestion, audioChild)

                print(answerA)
                print(answerB)
                print(answerC)
                print(answerD)
                insertAnswer(idQuestion, answerA['content'], answerA['audio'])
                insertAnswer(idQuestion, answerB['content'], answerB['audio'])
                insertAnswer(idQuestion, answerC['content'], answerC['audio'])
                if idTypeTopic == 1:
                    insertAnswer(idQuestion, answerD['content'], answerD['audio'])
                answer_type = checkAnswerTopicType12(driver)
                print(answer_type)
                if answer_type == 1:
                    insertAnswerQuestion(idQuestion, answerA['content'])
                elif answer_type == 2:
                    insertAnswerQuestion(idQuestion, answerB['content'])
                elif answer_type == 3:
                    insertAnswerQuestion(idQuestion, answerC['content'])
                elif answer_type == 4:
                    insertAnswerQuestion(idQuestion, answerD['content'])
            else:
                deleteQuestion(idQuestion)
        else:
            deleteQuestion(idQuestion)

    driver.find_element_by_xpath('//*[@id="choices"]/input[1]').click()
    s = bs4.BeautifulSoup(driver.page_source, 'lxml')
    nextText = s.select_one('div.panel-body > #testfooter > #nextbutton > input').attrs['value']
    if 'Next' in nextText:
        driver.find_element_by_xpath('//*[@id="nextbutton"]').click()
        driver.implicitly_wait(5)
        s = bs4.BeautifulSoup(driver.page_source, 'lxml')
        getQuestionType1Or2(driver, s, idTypeTopic, topicId)
    else:
        if idTypeTopic == 1:
            main('https://www.examenglish.com/TOEIC/TOEIC_listening_part2.htm')
        else:
            main('https://www.examenglish.com/TOEIC/TOEIC_listening_part3.htm')


def checkAnswerTopicType12(driver):
    driver.find_element_by_xpath('//*[@id="choices"]/input[1]').click()
    s = bs4.BeautifulSoup(driver.page_source, 'lxml')
    answerQuestion = s.select_one('div.panel-body > #centreposition > #col1 > #form1').text
    if 'Correct' in answerQuestion:
        return 1
    driver.find_element_by_xpath('//*[@id="choices"]/input[2]').click()
    s = bs4.BeautifulSoup(driver.page_source, 'lxml')
    answerQuestion = s.select_one('div.panel-body > #centreposition > #col1 > #form1').text
    if 'Correct' in answerQuestion:
        return 2
    driver.find_element_by_xpath('//*[@id="choices"]/input[3]').click()
    s = bs4.BeautifulSoup(driver.page_source, 'lxml')
    answerQuestion = s.select_one('div.panel-body > #centreposition > #col1 > #form1').text
    if 'Correct' in answerQuestion:
        return 3
    driver.find_element_by_xpath('//*[@id="choices"]/input[4]').click()
    s = bs4.BeautifulSoup(driver.page_source, 'lxml')
    answerQuestion = s.select_one('div.panel-body > #centreposition > #col1 > #form1').text
    if 'Correct' in answerQuestion:
        return 4
    return -1


def deleteQuestion(idQuestion):
    connection = conn()
    cursor = connection.cursor()
    sql = "DELETE FROM question WHERE id = %s"
    val = idQuestion
    cursor.execute(sql, val)
    connection.commit()


def downloadFile(dir, path, isImage, isAudio=False, isAudioQuestion=False, typeId=None):
    # tạo thư mục
    global url, file_name
    if not os.path.isdir(dir):
        os.mkdir(dir)

    if isImage:
        file_name = path.split('images/')[1].lower()
    else:
        file_name = path.split('audio/')[1].lower()
        if isAudioQuestion:
            file_name = 'audio_question_type%s_%s' % (typeId, file_name)

    if os.path.exists(dir + "/" + file_name):
        if isImage:
            return file_name
        else:
            if isAudio:
                return file_name
            else:
                return dir + '/' + file_name

    url = "https://www.examenglish.com/TOEIC/" + path
    print(url)

    ua_str = UserAgent().chrome
    response = requests.get(url, stream=True, headers={"User-Agent": ua_str})
    if response.status_code == 404:
        print('Error Not Found')
        print(url)
        return None
    with open(dir + '/' + file_name, 'wb') as out_file:
        out_file.write(response.content)

    print(response.status_code)
    print(response.headers['content-type'])

    if isImage:
        return file_name
    else:
        if isAudio:
            return file_name
        else:
            return dir + '/' + file_name


def insertTopicType(title, description, description_1, topicId):
    connection = conn()
    cursor = connection.cursor()
    sql = "SELECT  id FROM topictype WHERE title = %s"
    val = title
    cursor.execute(sql, val)
    id = cursor.fetchone()
    if not id or not id['id']:
        sql = "INSERT INTO `topictype` (idTopic ,title, recommend, instruction) VALUES (%s,%s, %s, %s)"
        val = (topicId, title, description, description_1)
        cursor.execute(sql, val)
        connection.commit()
        return cursor.lastrowid
    else:
        return id['id']


def insertQuestion(idTypeTopic, topicId, image=None, content=None, audio=None):
    connection = conn()
    cursor = connection.cursor()
    isValid = False
    if image:
        sql = """SELECT  id FROM question WHERE image = %s"""
        val = image
        id = cursor.execute(sql, val)
        if id == 0:
            isValid = True
    if content:
        sql = """SELECT  id FROM question WHERE content = %s"""
        val = content
        id = cursor.execute(sql, val)
        if id == 0:
            isValid = True
    if audio:
        sql = """SELECT  id FROM question WHERE audio = %s"""
        val = audio
        id = cursor.execute(sql, val)
        if id == 0:
            isValid = True

    if isValid:
        sql = "INSERT INTO `question` (topicId ,topicTypeId, image, audio ,audioChild, content) VALUES (%s,%s, %s, %s,%s,%s)"
        val = (topicId, idTypeTopic, image, audio, None, content)
        cursor.execute(sql, val)
        connection.commit()
        return cursor.lastrowid
    else:
        return -1


def insertQuestionChild(idQuestion, content):
    connection = conn()
    cursor = connection.cursor()
    sql = "INSERT INTO `questionchild` (id_question ,content) VALUES (%s,%s)"
    val = (idQuestion, content)
    cursor.execute(sql, val)
    connection.commit()
    return cursor.lastrowid

def insertAnswer(idQuestion, content, audio=None, questionChildId=None):
    connection = conn()
    cursor = connection.cursor()
    sql = "INSERT INTO `answer` (questionId ,questionChildId, content, audio) VALUES (%s,%s, %s, %s)"
    val = (idQuestion, questionChildId, content, audio)
    cursor.execute(sql, val)
    connection.commit()


def insertAnswerQuestion(idQuestion, content, questionChildId=None):
    connection = conn()
    cursor = connection.cursor()
    sql = "INSERT INTO `answerquestion` (questionId ,questionChildId, content) VALUES (%s, %s, %s)"
    val = (idQuestion, questionChildId, content)
    cursor.execute(sql, val)
    connection.commit()


def updateQuestion(idQuestion, audio, audioChild=None):
    connection = conn()
    cursor = connection.cursor()
    if audioChild:
        print(audio)
        print(audioChild)
        sql = "UPDATE question SET audio = %s , audioChild = %s WHERE id = %s"
        val = (audio, audioChild, idQuestion)
    else:
        sql = "UPDATE question SET audio = %s WHERE id = %s"
        val = (audio, idQuestion)
    cursor.execute(sql, val)
    connection.commit()

if __name__ == '__main__':
    # topicType = LISTENING
    # main('https://www.examenglish.com/TOEIC/TOEIC_listening_part1.htm')
    topicType = READING
    main('https://www.examenglish.com/TOEIC/TOEIC_reading.htm')
