# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class UNDPJobDataItem(scrapy.Item):
    englishname = scrapy.Field() #组织英文缩写
    chinesename = scrapy.Field() #组织中文名称
    incontinent = scrapy.Field() #组织所属洲
    incountry = scrapy.Field()   #组织所在国家
    type = scrapy.Field()        #组织类别
    url = scrapy.Field()         #组织主页
    alljoburl = scrapy.Field()   #组织招聘岗位主页
    joburl = scrapy.Field()      #该招聘岗位主页


    describe = scrapy.Field()    #岗位描述
    suoshu = scrapy.Field()      #所属机构
    work = scrapy.Field()        #岗位名称
    applytime = scrapy.Field()   #申请截止时间
    linkman = scrapy.Field()     #岗位联系人


    Location = scrapy.Field()    #位置
    ApplicationDeadline = scrapy.Field() #申请截至时间
    TypeofContract = scrapy.Field() #包工方式
    PostLevel = scrapy.Field()   #职位级别
    LanguagesRequired = scrapy.Field()   #语言要求
    DurationofInitialContract = scrapy.Field()   #初始合同时间
    ExpectedDurationofAssignment = scrapy.Field()   #预计工作时间
    AdditionalCategory  = scrapy.Field()   #额外的类别


    Background = scrapy.Field()         #背景
    DutiesandResponsibilities = scrapy.Field()           #工作职责
    Competencies = scrapy.Field()       #能力
    RequiredSkillsandExperience = scrapy.Field()        #技能和经历

class UNDPJobDataItem2(scrapy.Item):

    englishname = scrapy.Field() #组织英文缩写
    chinesename = scrapy.Field() #组织中文名称
    incontinent = scrapy.Field() #组织所属洲
    incountry = scrapy.Field()   #组织所在国家
    type = scrapy.Field()        #组织类别
    url = scrapy.Field()         #组织主页
    alljoburl = scrapy.Field()   #组织招聘岗位主页
    joburl = scrapy.Field()      #该招聘岗位主页

    describe = scrapy.Field()    #岗位描述
    suoshu = scrapy.Field()      #所属机构
    Title = scrapy.Field()        #岗位名称
    applytime = scrapy.Field()   #申请截止时间
    linkman = scrapy.Field()     #岗位联系人

    PracticeArea = scrapy.Field()     #实习区
    VacancyEndDate = scrapy.Field()   #工作地点
    Experience = scrapy.Field()   #教育和工作经历
    Grade = scrapy.Field()   #职级
    VacancyType = scrapy.Field()  # 空缺类型
    Bureau = scrapy.Field()  # 办公室
    ContractDuration = scrapy.Field()  # 合同期
    Languages = scrapy.Field()  # 语言

    Background = scrapy.Field()         #背景
    DutiesandResponsibilities = scrapy.Field()        #义务与责任
    Competencies = scrapy.Field()       #能力
    RequiredSkillsandExperience = scrapy.Field()        #技能和经历
    Disclaimer = scrapy.Field()        #免责


# class ITERjobDataItem2(scrapy.Item):

#     englishname = scrapy.Field() #组织英文缩写
#     chinesename = scrapy.Field() #组织中文名称
#     incontinent = scrapy.Field() #组织所属洲
#     incountry = scrapy.Field()   #组织所在国家
#     type = scrapy.Field()        #组织类别
#     url = scrapy.Field()         #组织主页
#     alljoburl = scrapy.Field()   #组织招聘岗位主页
#     joburl = scrapy.Field()      #该招聘岗位主页

class ITERjobDataItem(scrapy.Item):
    
    JobTitle = scrapy.Field()
    JobDetailUrl = scrapy.Field()

    MainJob = scrapy.Field()
    Department = scrapy.Field()
    Division = scrapy.Field()
    Section = scrapy.Field()
    JobFamily = scrapy.Field()
    ApplicationDeadline = scrapy.Field()
    Grade = scrapy.Field()
    DirectEmployment = scrapy.Field()
    Purpose = scrapy.Field()
    MainDuties = scrapy.Field()
    MeasuresOfEffectiveness = scrapy.Field()
    LevelOfExperience = scrapy.Field()
    Knowledge = scrapy.Field()
    SocialSkills = scrapy.Field()
    SpecificSkills = scrapy.Field()
    GeneralSkills = scrapy.Field()
    Others = scrapy.Field()
    Languages = scrapy.Field()
