import os, zipfile, shutil, json
import xml.etree.cElementTree as ET
from lxml import etree
from xml.dom import minidom

def apply(func,arg):
    answer = func(arg)
    return answer



class File:
    def name(file):
        name = file.rpartition('.')[0]
        return name
    def ext(file):
        ext = file.rpartition('.')[-1]
        return ext
    def isDoc(self,file):
        ext = self.ext(file)
        if ext=="doc" or ext=="DOC":
            return True
        else: return False
    def isXML(self,file): # determines if file has .xml extension
        ext = self.ext(file)
        if ext=='xml': return True
        else: return False
    def isPDf(self,file):
        ext = self.ext(file)
        if ext=="PDF" or ext=="pdf":
            return True
        else: return False   
    def isDocx(self,file):
        ext = self.ext(file)
        if ext=="DOCX" or ext=="docx":
            return True
        else: return False             
    def isEmpty(filepath):
        if os.stat(filepath).st_size == 0:
            return True
        else: return False
class Storage:
    def createFolderForFile(input_directory,output_directory,condition):
        for file in os.listdir(input_directory):
            if apply(condition,file):
                original_filepath = os.path.join(input_directory,file)
                with open(original_filepath,'r') as f:
                    file_read = f.read()
                for folder in os.listdir(output_directory):
                    if File.name(file)==folder:
                        new_filepath = os.path.join(output_directory,folder,file)
                        with open(new_filepath,'w') as f:
                            f.write(file_read)
    def createNewFolder(directory,name):
        folderpath = os.path.join(directory,name)
        if not os.path.exists(folderpath): os.mkdir(folderpath)
        return folderpath
    class Delete:
        def FilesDifferentFromType(directory,condition1,condition2):
            for folder in os.listdir(directory):
                if not condition1(folder,".DS"): #put General.contains()
                    for file in os.listdir(os.path.join(directory,folder)):
                        if not condition2(file):
                            filepath = os.path.join(directory,folder,file)
                            os.remove(filepath)
        def FilesOfType(directory,condition1,condition2):
            for folder in os.listdir(directory):
                if not condition1(folder,".DS"): #put General.contains()
                    for file in os.listdir(os.path.join(directory,folder)):
                        if condition2(file):
                            filepath = os.path.join(directory,folder,file)
                            os.remove(filepath)
        def FilesOfVariousTypes(directory,extensions,condition1,condition2):
            for folder in os.listdir(directory):
                if not condition1(folder):
                    folder_directory = os.path.join(directory,folder)
                    for file in os.listdir(folder_directory):
                        file_extension = os.path.splitext(file)
                        if not condition2(extensions,file_extension):
                            os.remove(os.path.join(folder_directory,file))
    class Check:
        def ifDifferentExtension(directory,filename,extension): #check if file.example shares folder with file.example2
            filepath = os.path.join(directory,filename+extension)
            if os.path.exists(filepath):
                return True
            else: return False
        def fileInFolderMeetCondition(directory,condition):
            return any(condition(file) for file in os.listdir(directory))
    class Move:
        def toNestedDirectory(temporary_directory,output_directory,condition):
            for file in os.listdir(temporary_directory):
                if condition(file):
                    filename = Treaty.getName(file)
                    for folder in os.listdir(output_directory):
                        folder_directory = os.path.join(temporary_directory,folder)
                        if filename == folder:
                            original_filepath = os.path.join(folder_directory,file)
                            new_filepath = os.path.join(folder_directory,file)
                            if not os.path.exists(new_filepath):
                                shutil.move(original_filepath,new_filepath)
        def filesOfSpecificType(temporary_directory,output_directory,condition1,condition2):
            for folder in os.listdir(output_directory):
                if condition1(folder,".DS"):
                    folder_directory = os.path.join(output_directory,folder)
                    for file in os.listdir(folder_directory):
                        if condition2(file):
                            original_filepath = os.path.join(folder_directory,file)
                            new_filepath = os.path.join(temporary_directory,file)
                            if not os.path.exists(original_filepath,new_filepath):
                                shutil.move(original_filepath,new_filepath)
class Treaty: #used for dealing with stored files
    def typeOfSource(filename):
        if "full" in filename and "annex" in filename:
            return 2 
        elif "annex" in filename:
            return 1
        else: 
            return 0
    def inEnglish(filename):
        if "en" in filename:
            return True
        else: return False
    def getName(filename):
        if "-" in filename:
            name = filename.rpartition('-')[0]
            return name
        else: return filename
    def categorizeSource(filename):
        if "." in filename:
            category = filename.rpartition('-')[2].rpartition('.')[0].rpartition('_')[0]
        else: 
            category = filename.rpartition('-')[2].rpartition('_')[0]
        return category
    class Search:
        def annexEn(self,directory):
            for file in os.listdir(directory):
                if Treaty.typeOfSource(file)==1 and Treaty.inEnglish(file):
                    return os.path.join(directory,file)
            return self.annex(directory)
        def annex(directory):
            for file in os.listdir(directory):
                if Treaty.typeOfSource(file)==1:
                    return os.path.join(directory,file)
        def fullEn(self,directory):
            for file in os.listdir(directory):
                if Treaty.typeOfSource(file)==0 and Treaty.inEnglish(file):
                    return os.path.join(directory,file)
            return self.full(directory)
        def full(directory):
            for file in os.listdir(directory):
                if Treaty.typeOfSource(file)==0:
                    return os.path.join(directory,file)        
        def sourceInFolder(directory):
            boolvalue = Storage.Check.fileInFolderMeetCondition(directory,File.isPDf)   
            return boolvalue             

class parseJSON:
    class General:
        def keys(json_object):
            thekeys = [key for key in json_object]
            return thekeys
        def haskey(json_object,json_key):
            if json_key in [k for k in json_object]:
                return True
            return False
    class extract:
        def path(json_object):
            return json_object['Path'][11:]
        def text(json_object):
            return json_object['Text']
        def font_weight(json_object):
            return json_object['Font']['weight']
        def text_attributes(json_object):
            return json_object['attributes']
        def text_alignment(json_object):
            if parseJSON.General.haskey(json_object,'attributes'):
                if parseJSON.General.haskey(parseJSON.extract.text_attributes(json_object),'TextAlign'):
                    return parseJSON.extract.text_attributes(json_object)['TextAlign']
            return 'x' # (Center, Justify, etc.)
        def text_size(json_object):
            return json_object['TextSize']
        def bounds(json_object):
            return json_object['Bounds']
        def page(json_object):
            return json_object['Page']
        def font_weight(json_object):
            return json_object['Font']['weight']
    class parsing:
        def noHighWordsTag(section_object):
            for highWord in highLevelWords:
                if highWord in section_object[1].lower():
                    rest_of_string = section_object[1].lower().replace(highWord,"")
                    return rest_of_string
        def sectionNumberName(objects_list,section_object):
            rest_string = parseJSON.parsing.noHighWordsTag(section_object).strip()
            if rest_string.isnumeric(): 
                return [
                    [section_object[1].strip()],
                    [parseJSON.find.section_name(objects_list)]
                ]
            else:
                if (rest_string.isalpha()):
                    return [
                        [section_object[1].strip()],
                        [parseJSON.find.section_name(objects_list)]
                    ]
                else:
                    for symb in symbolList:
                        if symb in rest_string: return [
                            [section_object[1].rpartition(symb)[0].strip()],
                            [section_object[1].rpartition(symb)[-1].strip()]
                            ]
        def subsectionNumberName(objects_list, subsection_object):
            rest_string = parseJSON.parsing.noHighWordsTag(subsection_object).strip()
            if rest_string.isnumeric(): 
                return [
                    subsection_object[1].strip(),
                    parseJSON.find.section_name(objects_list)
                ]
            else:
                if (rest_string.isalpha()):
                    return [
                        subsection_object[1].strip(),
                        parseJSON.find.section_name(objects_list)
                    ]
                else:
                    for symb in symbolList:
                        if symb in rest_string: return [
                            subsection_object[1].rpartition(symb)[0].strip(),
                            subsection_object[1].rpartition(symb)[-1].strip()
                            ]
        def typeOfHighWord(section_object):
            for highWord in highLevelWords:
                if highWord in section_object[1].lower().strip():
                    return highWord
            return ''        
        def articleNumberName(objects_list,json_object):
            name = json_object[1]            
            for symb in symbolList:
                if symb in name:
                    name = name.lower().strip().replace(symb, "")
            for num in under10:
                if str(num) in name:
                    name = name.replace(str(num),"")
            name = name.lower().replace("article","").strip()            
            if name=="":
                name = parseJSON.find.article_name(objects_list)
            number = (json_object[1].lower().replace(name,"").strip() if name in json_object[1].lower() else json_object[1].lower().strip())
            for symb in symbolsInArticle:
                if symb in number:
                    number = number.replace(symb,"")
            return [number.capitalize(),name.capitalize()]
        def typeOfSection(section_object):
            for buzz in buzzwords:
                if buzz in section_object[1].lower():
                    return buzz
            return ''
    class categorize:
        def run(path_key):  # output classification (e.g. TABLE, P, etc.) + ([1][2][...])
            category = path_key
            main_category = category[:category.index("/")] if "/" in category else category
            return main_category              
    class find:
        def title(objects_list):
            output_json_list = []; object_to_append = 0
            for json_object in objects_list:
                if parseJSON.logical.isTitle(objects_list,json_object):
                    object_to_append = [[json_object[1]],[]]
                    output_json_list.append(object_to_append)                    
                    return output_json_list
        def section_name(objects_list):
            for json_object in objects_list:
                if(
                    (json_object[2]==700)
                    or 
                    (parseJSON.logical.isTopInPage(objects_list,json_object))
                    or 
                    ("Center" in json_object[5])                    
                ): return json_object[1]
            return ''
        def sectionNumberName(next_object, section_object):            
            notag = section_object[1].lower().replace(parseJSON.parsing.typeOfHighWord(section_object),"")
            if ":" in notag: 
                return [section_object[1].split(":")[0].strip(),section_object[1].split(":")[-1].strip()]
            elif (
                (next_object[2]==section_object[2] and next_object[4]==section_object[4])
                or
                (next_object[2]==section_object[2] and next_object[4]==section_object[4])
                or
                (next_object[3]==section_object[3] and "Center" in next_object[4])
            ): return [section_object[1].strip(),next_object[1].strip()]
            return [section_object[1].strip(),""]
        def articleNumberName(next_object,article_object):
            notag = article_object[1].lower().replace("article","")
            if ":" in notag: 
                return [article_object[1].split(":")[0].strip(),article_object[1].split(":")[-1].strip()]
            elif(
                "Center" in next_object[4]
                or
                next_object[2]==700
            ): return[article_object[1].strip(),next_object[1].strip()]
            else: return [article_object[1].strip(),""]
        
        def mainSection(objects_list):
            for json_object in objects_list:
                if parseJSON.logical.isMainTag(
                    objects_list[objects_list.index(json_object):], json_object
                ):
                    return parseJSON.parsing.typeOfHighWord(json_object)
            return ''
        def article_name(objects_list):
            for json_object in objects_list:
                if "article" not in json_object[1].lower():
                    if(
                        json_object[2]==700 or "Center" in json_object[4]
                    ):
                        return json_object[1]
                elif parseJSON.logical.isArticleTag(json_object): return ""
            return ""
        def allSections(objects_list):
            return_list = []
            for json_object in objects_list:
                if parseJSON.logical.isMainTag(objects_list, json_object):                    
                    return_list.append(json_object[1])
            return return_list
        def mainSectionsInPostBody(objects_list):            
            return [parseJSON.find.sectionNumberName(objects_list[objects_list.index(json_object)+1],json_object) for json_object in objects_list if parseJSON.logical.isComplementTag(objects_list,json_object)]                            
        
        def subsectionTagInSection(objects_list,avoidtags): # return search tag name        
            for json_object in objects_list:
                if parseJSON.logical.isMainTag(objects_list,json_object) and not any(json_object[1].lower().startswith(avoidtag) for avoidtag in avoidtags):
                    return parseJSON.parsing.typeOfHighWord(json_object)
            return ""
        def thisSectionTags(objects_list,searchtag): # return all [num] and [name] for x section
            i = 0; num = []; name = []; num_name_out = []
            while (i < len(objects_list)-1):
                if (parseJSON.logical.isMainTag(objects_list,objects_list[i]) 
                and objects_list[i][1].lower().startswith(searchtag)):
                    num_name = parseJSON.find.sectionNumberName(objects_list[i+1],objects_list[i])
                    num_name_out.append(num_name)
                    #num.append(num_name[0]); name.append(num_name[1])
                i+=1
            return num_name_out         
        def startOfSection(objects_list,num_name): #num_name = [num, name], no nested list
            if num_name[1]!="":
                for obj in objects_list:                                                            
                    if num_name[1] in obj[1]: return objects_list.index(obj)+1                    
            else:
                for obj in objects_list:
                    if obj[1].lower().startswith(num_name[0]): return objects_list.index(obj)+1
        def endOfSection(objects_list,num_name): #num_name = [num, name], no nested list
            for obj in objects_list:
                if obj[1].startswith(num_name[0]):                     
                    return objects_list.index(obj)                
        def divideSection(objects_list,num_name): # return indeces for each subsect in x sect
            indices = []; i = 0            
            while (i < len(num_name)):
                if (i+1)>=len(num_name):
                    indices.append([parseJSON.find.startOfSection(objects_list,num_name[i]),
                    len(objects_list)])
                else:
                    indices.append([parseJSON.find.startOfSection(objects_list,num_name[i]),
                    parseJSON.find.endOfSection(objects_list,num_name[i+1])])
                i+=1
            return indices
        def section(objects_list:list, indices:list, num_name:list, avoidtags:list):
            #for y in num_name: print(y,end="\n---------")
            num_name_main = num_name; avoidtags = avoidtags
            for index in indices:                
                if index[1]<len(objects_list):                
                    objects_list_temp = objects_list[index[0]:index[1]]
                else:
                    objects_list_temp = objects_list[index[0]:]
                searchtag = parseJSON.find.subsectionTagInSection(objects_list_temp,avoidtags)
                if searchtag!="":
                    avoidtags.append(searchtag)
                    num_name_inner = parseJSON.find.thisSectionTags(objects_list_temp,searchtag)
                    indices_inner = parseJSON.find.divideSection(objects_list_temp,num_name_inner)
                    for num in num_name_inner[0]: num_name_main[0].append(num)
                    for name in num_name_inner[1]: num_name_main[1].append(name)
                    return parseJSON.find.section(objects_list_temp,indices_inner,num_name_inner,avoidtags)
                else: continue
            return num_name_main
        def mainsection(objects_list): 
            i = 0; avoidtags = []; num_name = []
            searchtag = parseJSON.find.subsectionTagInSection(objects_list,avoidtags)            
            if searchtag!="": 
                avoidtags.append(searchtag)
                num_name = parseJSON.find.thisSectionTags(objects_list,searchtag)
                #print(num_name)
                indices = parseJSON.find.divideSection(objects_list,num_name)
                return indices
                #return parseJSON.find.section(objects_list,indices,num_name,avoidtags)   
            else:
                return
                #return parseJSON.structure.hierarchySchema.searchFor.articles(objects_list)

        
        class indexOf:
            def Title(objects_list):
                title_index = 0
                for json_object in objects_list:
                    if parseJSON.logical.isTitle(objects_list,json_object):
                        title_index = objects_list.index(json_object)
                        break
                return title_index
            def PreambleTag(objects_list):
                preamble_index = 0                
                for json_object in objects_list:
                    if parseJSON.logical.isPreambleTag(
                        objects_list,
                        json_object
                    ): 
                        preamble_index = objects_list.index(json_object)
                        return preamble_index
                return parseJSON.find.indexOf.Title(objects_list)+1
            class endOf:
                def Preamble(objects_list):                    
                    end_of_preamble = 0
                    for json_object in objects_list:
                        if parseJSON.logical.isMainTag(
                            objects_list,json_object
                        ):
                            end_of_preamble = objects_list.index(json_object)
                            break
                    return end_of_preamble
                def preambletag(objects_list):
                    for json_object in objects_list:
                        if "have agreed as follows:" in json_object[1].lower():
                            return objects_list.index(json_object)                    
                def body(objects_list):
                    for json_object in objects_list:
                        if "for the government of" in json_object[1].lower():
                            return objects_list.index(json_object)
    class logical:
        def isTopInPage(objects_list,json_object): 
            initial = [obj[5][3] for obj in objects_list if obj[6]==json_object[6]]            
            return all(x < json_object[5][3] for x in initial[initial.index(json_object[5][3])+1:])
        def isMainTag(objects_list,json_object):
            if(
                any(json_object[1].lower().startswith(highWord) for highWord in highLevelWords)
                and
                (json_object[2]==700 or parseJSON.logical.isTopInPage(objects_list,json_object))
                and 
                (not any(lowWord in json_object[0].lower() for lowWord in lowLevelWords))
                and #just added
                "Center" in json_object[4] #just added
            ): return True
            else: return False                       
        def isSubsectionTag(json_object,section_tags):
            if(
                any(highWord in json_object[1].lower() for highWord in highLevelWords)
                and 
                not any(section_tag in json_object[1].lower() for section_tag in section_tags)
                and 
                json_object[2]==700
                and
                (not any(lowWord in json_object[0].lower() for lowWord in lowLevelWords))
                and
                (not any(lowWord in json_object[1].lower() for lowWord in lowLevelWords))
            ): return True
            else: return False
        def isPreambleTag(objects_list,json_object):
            if(
                all(highWord in json_object[1].lower() for highWord in highLevelWords)==False
                and
                (json_object[2]==700 or parseJSON.logical.isTopInPage(objects_list,json_object))
                and
                (not any(lowWord in json_object[0].lower() for lowWord in lowLevelWords))
                and 
                "preamble" in json_object[1].lower()
            ):
                return True
            else: return False
        def isTitle(objects_list,json_object):
            if(
                ("H" in json_object[0] or "Center" in json_object[5])
                and parseJSON.logical.isTopInPage(objects_list,json_object)
            ):  return True
            else:
                if(
                    "H1" in json_object[0]
                    or "Title" in json_object[0]
                ): return True
                else: 
                    if(
                        "H2" in json_object[0]
                    ): return True
            return False
        def hasSubsection(objects_list, section_tags):
            return_value = False
            for json_object in objects_list:
                if(parseJSON.logical.isMainTag(
                    objects_list[objects_list.index(json_object):], json_object
                )):
                        if any(section_tag in json_object[1].lower() for section_tag in section_tags):
                            break
                        else:
                            if not any(low in json_object[1].lower() for low in lowLevelWords):
                                return_value = True
            return return_value
        def isArticleTag(json_object):
            if not any(lowtype in json_object[0].lower() for lowtype in lowType):
                if (json_object[1].lower().strip().startswith('article')):
                    x = json_object[1].lower().replace("article","").strip()
                    if any(x.startswith(str(num)) for num in under10): return True          
                elif any(json_object[1].lower().strip().startswith(str(num)) for num in under10) and json_object[2]==700: return True
            return False
        def SupplementIsFirstSection(objects_list):
            for json_object in objects_list:
                if parseJSON.logical.isMainTag(objects_list[objects_list.index(json_object):],json_object):
                    if "annex" in json_object[1].lower() or "protocol" in json_object[1].lower():
                        return True                        
                    else:
                        return False
        def isComplementTag(objects_list, json_object):
            if(
                any(json_object[1].lower().startswith(postword) for postword in postBodyWords)
                #any(highWord in json_object[1].lower() for highWord in highLevelWords)
                and
                (json_object[2]==700 or parseJSON.logical.isTopInPage(objects_list,json_object))
                and 
                (not any(lowWord in json_object[0].lower() for lowWord in lowLevelWords))
            ): return True
            else: return False             
            return       
        def noMainSection(objects_list):
            if not all(parseJSON.logical.isMainTag(objects_list,json_object) for json_object in objects_list
            ): return True
            return False
    class structure:
        def byObject(jsondata): # filters out TABLES, outputs list
            filtered = []
            for object in jsondata['elements']:
                if ("Text" in parseJSON.General.keys(object)
                    and "Table" not in parseJSON.extract.path(object)):
                    textalign = parseJSON.extract.text_alignment(object)  #initialize textalign
                    filtered.append([
                            parseJSON.categorize.run(parseJSON.extract.path(object)), #category
                            parseJSON.extract.text(object), #text
                            parseJSON.extract.font_weight(object), #weight of font
                            parseJSON.extract.text_size(object), #size of text
                            textalign, # alignment of object
                            parseJSON.extract.bounds(object), # 4-points bounds    
                            parseJSON.extract.page(object) # page location of object            
                    ])
            return filtered   
        class hierarchySchema:
            class searchFor:
                def SubSections(section_tags, objects_list, json_list, section):
                    next_section_found = False; return_list = json_list; ind=0
                    sectionNumber = section[0]; sectionName = section[1]
                    while not next_section_found:                    
                        ind+=1
                        if ind>=len(objects_list): break
                        else:                
                            if parseJSON.logical.isMainTag(objects_list[ind:],objects_list[ind]):                        
                                if parseJSON.logical.isSubsectionTag(objects_list[ind],section_tags):    
                                    subsection = parseJSON.parsing.subsectionNumberName(
                                        objects_list[ind+1:],
                                        objects_list[ind]
                                    )
                                    sectionNumber.append(subsection[0])
                                    sectionName.append(subsection[1])
                                    section_tags.append(parseJSON.parsing.typeOfHighWord(objects_list[ind]))
                                    if parseJSON.logical.hasSubsection(
                                        objects_list[ind:], section_tags
                                    ):
                                        return parseJSON.structure.hierarchySchema.searchFor.SubSections(
                                            section_tags,objects_list[ind:],return_list,[sectionNumber,sectionName]
                                        )
                                    else:
                                        return_list.append([sectionNumber, sectionName])                
                                    sectionNumber = [sectionNumber[0]]
                                    sectionName = [sectionName[0]]
                                    section_tags.remove(parseJSON.parsing.typeOfHighWord(objects_list[ind]))
                                else:
                                    next_section_found = True                    
                    return return_list, ind                        
                def Sections(section_tag,ind,objects_list, schema_list):
                    section_tags = [section_tag] # the section tags found so far
                    while(ind < len(objects_list)):
                        if(
                            parseJSON.logical.isMainTag(objects_list[ind:],objects_list[ind])
                            and section_tag in objects_list[ind][1].lower()
                        ):
                            section = parseJSON.parsing.sectionNumberName(
                                objects_list[ind+1:], objects_list[ind]
                            )
                            if parseJSON.logical.hasSubsection(objects_list[ind:], section_tags):                    
                                schema_list, end_section_ind = parseJSON.structure.hierarchySchema.searchFor.SubSections(
                                    section_tags, objects_list[ind:], schema_list, section
                                )
                                ind = end_section_ind
                            else:
                                schema_list.append(section)
                        ind+=1
                    return schema_list
                def articles(objects_list):
                    section_articles = []
                    for json_object in objects_list:
                        if parseJSON.logical.isArticleTag(json_object):
                            to_append = parseJSON.find.articleNumberName(
                                objects_list[objects_list.index(json_object)+1],json_object
                            )
                            #to_append = parseJSON.parsing.articleNumberName(objects_list[objects_list.index#(json_object)+1:],json_object)
                            section_articles.append(to_append)
                    return section_articles
            def get(jsondata):
                objects_list = parseJSON.structure.byObject(jsondata)
                schema_list = parseJSON.find.title(objects_list)
                ind = parseJSON.find.indexOf.Title(objects_list) + 1                
                main_section = parseJSON.find.mainSection(objects_list[ind:])
                return parseJSON.structure.hierarchySchema.searchFor.Sections(main_section,ind,objects_list,schema_list)                                                
            def indices(jsondata):  # between these ranges there is only section content/text                
                schema = parseJSON.structure.hierarchySchema.get(jsondata)
                objects_list = parseJSON.structure.byObject(jsondata)                
                preamble_starts = parseJSON.find.indexOf.PreambleTag(objects_list)
                preamble_ends = parseJSON.find.indexOf.endOf.Preamble(objects_list)
                index_ranges = []; index_ranges.append([preamble_starts+1,preamble_ends])                
                for json_object in objects_list:
                    if schema[1][0][len(schema[1][0])-1] in json_object[1]: 
                        index_range = [objects_list.index(json_object)+1]
                        break
                for scheme in schema[2:]:
                    for json_object in objects_list:
                        if scheme[0][len(scheme[0])-1] in json_object[1]:
                            index_range.append(objects_list.index(json_object))
                            break
                    if len(index_range)==2:
                        index_ranges.append(index_range)
                        search_term = scheme[1][len(scheme[1])-1]
                        for json_object in objects_list:
                            if search_term in json_object[1]:
                                index_range = [objects_list.index(json_object)+1]
                                break                        
                index_ranges.append([index_ranges[len(index_ranges)-1][1],len(objects_list)-1])
                return index_ranges  
                                                                                                  
        def get(jsondata):
            return_list = []
            idx_ranges = parseJSON.structure.hierarchySchema.indices(jsondata)
            objects_list = parseJSON.structure.byObject(jsondata)            
            for idx_range in idx_ranges:
                return_list.append(objects_list[idx_range[0]:idx_range[1]])
            return return_list
            

def main(jsondata, xml_filepath):
    textos = parseJSON.structure.get(jsondata)                                                      
    schema = parseJSON.structure.hierarchySchema.get(jsondata)
    XML.new(xml_filepath)
    XML.TreatyWriting.title(xml_filepath, schema[0][0][0])
    preambleText = " ".join([texto[1].strip() for texto in textos[0]])
    XML.TreatyWriting.preamble(xml_filepath,preambleText)
    for i in range(1,len(schema)):
        XML.TreatyWriting.new_chapter(
            xml_filepath, 
            ". ".join([str(num) for num in schema[i][0]]),
            ". ".join([str(nam) for nam in schema[i][1]])
        )        
        article = []
        for texto in textos[i]:
            if XML.schema.numberOfArticles(xml_filepath)==0:
                XML.TreatyWriting.new_article(xml_filepath,'-','Preamble')                        
            if parseJSON.logical.isArticleTag(texto):
                x = parseJSON.parsing.articleNumberName(textos[i][textos[i].index(texto)+1:],texto)
                XML.TreatyWriting.new_article(
                    xml_filepath,
                    x[0],
                    x[1]
                )
            else:

                XML.TreatyWriting.text_in_article(
                    xml_filepath,
                    (texto[1].replace("/"," or ").strip() if "/" in texto[1] else texto[1].strip())
                )

def test(jsondata):
    objects_list = parseJSON.structure.byObject(jsondata)
    schema_list = parseJSON.find.title(objects_list)
    end_preamble_ind = parseJSON.find.indexOf.endOf.preambletag(objects_list)
    end_body_ind = parseJSON.find.indexOf.endOf.body(objects_list)
    body_list = objects_list[end_preamble_ind:end_body_ind]
    complement_list = objects_list[end_body_ind:]    
    x = parseJSON.find.mainsection(body_list)
    #post_sections = parseJSON.find.mainSectionsInPostBody(complement_list)
    return x            
                            
class XML:
    class file:
        def isCorrupt(full_path): # tests for corrupt XML file
            with open(full_path,'r',encoding='utf-8') as f:
                try:
                    ET.parse(f)
                    return False
                except ET.ParseError:
                    return True
    class Parsing:
        def recover(filepath):
            parser = etree.XMLParser(recover=True)
            tree = etree.parse(filepath,parser)
            return tree.getroot()
        def standard(filepath):
            with open(filepath,'r',encoding='utf-8') as f:
                return ET.parse(f).getroot()
    class Content:
        def tagIsEmpty(tag):
            if tag.text is None or tag.text == "":
                return True
            else: return False
    def parse(self,filepath):
        if XML.file.isCorrupt(filepath): return XML.Parsing.recover(filepath)
        else: return XML.Parsing.standard(filepath)
    def prettify(filepath):  #apply correct indententation to xml
        xmlstr = minidom.parseString(ET.tostring(ET.parse(filepath).getroot())).toprettyxml(indent="\t")
        with open(filepath,'w') as f:
            f.write(xmlstr)    
    def new(filepath):  # create new xml treaty
        root = minidom.Document()
        xml = root.createElement('treaty')
        root.appendChild(xml)
        metaChild = root.createElement('meta')
        bodyChild = root.createElement('body')
        xml.appendChild(metaChild)
        xml.appendChild(bodyChild)
        xml_str = root.toprettyxml(indent="\t")
        with open(filepath,'w') as f:
            f.write(xml_str)
    class Storage:
        def CorruptXML(directory):
            corrupt_xml = []
            for file in os.listdir(directory):
                if File.isXML(file):
                    filepath = os.path.join(directory,file)
                    with open(filepath,'r',encoding='utf-8') as f:
                        if XML.file.isCorrupt(f): corrupt_xml.append(file)
            return corrupt_xml
    class TreatyWriting:
        def title(filepath, title):
            tree = ET.parse(filepath)
            root = tree.getroot()
            titletag = ET.SubElement(root[0],'name')
            titletag.text = title
            tree.write(filepath,encoding='utf-8',short_empty_elements=True)
        def new_chapter(filepath,number_input="",name_input=""):
            tree = ET.parse(filepath)
            root = tree.getroot()
            last_index = len(root) - 1
            ET.SubElement(root[last_index],'chapter',number=number_input,name=name_input,chapter_identifier="")
            tree.write(filepath,encoding='utf-8',short_empty_elements=False)
        def new_article(filepath,number_input="",name_input="",txt_input=""):
            tree = ET.parse(filepath)
            root = tree.getroot()
            last_index = len(root) - 1
            last_index_nested = len(root[last_index]) - 1
            article = ET.SubElement(root[last_index][last_index_nested],'article',number=number_input,name=name_input,chapter_identifier="")            
            article.text = txt_input
            tree.write(filepath,encoding='utf-8',short_empty_elements=False)
        def text_in_article(filepath,txt_input):
            tree = ET.parse(filepath)
            root = tree.getroot()
            idx = len(root) - 1
            idx2 = len(root[idx]) - 1
            idx3 = len(root[idx][idx2]) - 1
            article = root[idx][idx2][idx3]
            current_txt = article.text
            if current_txt != None:
                if any(current_txt.endswith(symb) for symb in symbolList):
                    article.text = " ".join([str(current_txt),txt_input])
                else:
                    article.text = ". ".join([str(current_txt),txt_input])
            else:
                article.text = txt_input
            tree.write(filepath,encoding='utf-8',short_empty_elements=True)
        def preamble(filepath, content):            
            XML.TreatyWriting.new_chapter(filepath,'-','Preamble')
            XML.TreatyWriting.new_article(filepath,'-','Preamble',content)            
    class schema:
        def numberOfChapters(filepath):
            tree = ET.parse(filepath)
            root = tree.getroot()            
            return len(root[1])      
        def numberOfArticles(filepath):
            tree = ET.parse(filepath)
            root = tree.getroot()
            bodyLength = len(root[1])
            if bodyLength==0: return 0            
            else: return len(root[1][bodyLength-1])

class ConvertJSONtoXML:
    class JSONoperations:
        def hasHighLevelWords(jsonfile):
            for seg in jsonfile:
                if len(seg)>1:
                    if any(hword in highLevelWords for hword in seg[0][1].lower()):
                        return True
            return False
    class XMLoperations:
        def addTitle(json_list,xml_filepath):
            for i,json_object in enumerate(json_list):
                if "title" in json_object[0][0].lower():
                    tree = ET.parse(xml_filepath)
                    root = tree.getroot()
                    if len(json_object)>2:
                        txt_input = " ".join([str(item) for item in json_object[3:]])
                    else: txt_input = ""
                    titletag_in_metadata = ET.SubElement(root[0],'name')
                    titletag_in_metadata.text = json_object[0][1]+json_object[1]+json_object[2]
                    tree.write(xml_filepath,encoding='utf-8',short_empty_elements=True)
                    XML.TreatyWriting.new_chapter(xml_filepath,"","Preamble")
                    XML.TreatyWriting.new_article(xml_filepath,"","Preamble",txt_input)
                    return i
        def hasTitle(xml_filepath):
            tree = ET.parse(xml_filepath)
            root = tree.getroot()
            if (len(root[0])>0):
                return True
            else: return False
    def unzipJSON(folderpath,filename,directory):
        zippath = os.path.join(folderpath,Treaty.getName(filename)+".zip")
        with zipfile.ZipFile(zippath,'r') as zip_ref:
            zip_ref.extractall(directory)
            os.rename(f"{directory}/{zip_ref.namelist()[0]}",f"{directory}/{filename}.json")
            os.remove(zippath)
    def parseJSON(filepath):
        with open(filepath,'r') as jsonfile:
            jsondata = json.load(jsonfile)
            treatyList = parseJSON.segmentByStructure(parseJSON,jsondata)
            return treatyList
    def JSONtoXML(self,jsonpath,xmlpath):
        XML.new(xmlpath)
        jsonsegments = self.parseJSON(jsonpath)
        cutoff = self.XMLoperations.addTitle(jsonsegments,xmlpath)
        if self.XMLoperations.hasTitle(xmlpath):
            if self.JSONoperations.hasHighLevelWords(jsonsegments):
                for seg in jsonsegments[cutoff+1:]:
                    if len(seg)>1 and self.JSONoperations.hasHighLevelWords(jsonsegments):
                        if any(hword in highLevelWords for hword in seg[0][1].lower()):
                            XML.TreatyWriting.new_chapter(xmlpath,seg[0][1],seg[1])
                        elif lowLevelWords in seg[0][1].lower():
                            txt_input = " ".join([str(item) for item in seg[2:]])
                            XML.TreatyWriting.new_article(xmlpath,seg[0][1],seg[1],txt_input)
                        else: pass
            else:
                XML.TreatyWriting.new_chapter(xmlpath,"","")
                for seg in jsonsegments[cutoff+1:]:
                    if lowLevelWords in seg[0][1].lower():
                        txt_input = " ".join([str(item) for item in seg[1:]])
                        XML.TreatyWriting.new_article(xmlpath,seg[0][1],seg[1],txt_input)
                    else: XML.TreatyWriting.new_chapter(xmlpath,seg[0][1],seg[1])
        else:
            if self.JSONoperations.hasHighLevelWords(jsonsegments):
                for seg in jsonsegments:
                    if len(seg)>1 and self.JSONoperations.hasHighLevelWords(jsonsegments):
                        if any(hword in highLevelWords for hword in seg[0][1].lower()):
                            XML.TreatyWriting.new_chapter(xmlpath,seg[0][1],seg[1])
                        elif lowLevelWords in seg[0][1].lower():
                            txt_input = " ".join([str(item) for item in seg[2:]])
                            XML.TreatyWriting.new_article(xmlpath,seg[0][1],seg[1],txt_input)
                        else: pass
            else:
                XML.TreatyWriting.new_chapter(xmlpath,"","")
                for seg in jsonsegments[cutoff:]:
                    if lowLevelWords in seg[0][1].lower():
                        txt_input = " ".join([str(item) for item in seg[1:]])
                        XML.TreatyWriting.new_article(xmlpath,seg[0][1],seg[1],txt_input)
                    else: XML.TreatyWriting.new_chapter(xmlpath,seg[0][1],seg[1])
        XML.prettify(xmlpath)





#-----------------------------------------------------------------------------------------------
headings = ["H1","H2","H3","H4","H5"]
highLevelWords = ['chapter','section','appendix','annex','protocol','part']
lowLevelWords = ['article','footnote','l[','p']
lowType = ['l[','p']
#mainBodyWords = ['chapter','section']
postBodyWords = ['annex','protocol','appendix','schedule']
buzzwords = ['chapter','section','article','appendix','annex','protocol','part']

under10 = [0,1,2,3,4,5,6,7,8,9]
symbolList = ['()','[]','.',':',';',',','+','-','*','/','&','|','<','>','=','~','$']
symbolsInArticle = ['()','[]',':',';',',','+','-','*','/','&','|','<','>','=','~','$']