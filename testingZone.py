import json
from re import L
from tkinter import PAGES

class DICTIONARY_METHODS:
    class logic:
        def hasKey(self,json_object:dict, key:str) -> bool:
            if key in [k for k in json_object]: return True 
            return False        
    class extract(logic):
        def keys(self,json_object: dict) -> list:
            """retrieve a list for the name of all attributes/keys 
            inside a JSON object            
            """      
            return [key for key in json_object]
        def path(self,json_object: dict) -> str:
            """returns the 'Path' attribute from a JSON object
            """
            path_string = json_object['Path'][11:]
            return (path_string[:path_string.index("/")] if "/" in path_string else path_string)
        def text(self,json_object: dict) -> str:
            return json_object['Text']
        def font_weight(self,json_object: dict) -> int:
            return json_object['Font']['weight']        
        def text_attributes(self,json_object: dict) -> dict:
            """returns the 'attributes' inner-object from a JSON object
            
            (aka.) attributes: {'LineHeight', 'SpaceAfter', 'TextAlign'}
            """        
            return json_object['attributes']
        def text_alignment(self,json_object: dict) -> str:            
            if self.hasKey(json_object,'attributes'):
                if self.hasKey(self.text_attributes(json_object),'TextAlign'):
                    return self.text_attributes(json_object)['TextAlign']
            return ''
        def text_size(self,json_object: dict) -> float:
            return json_object['TextSize']
        def bounds(self,json_object: dict) -> list:
            return json_object['Bounds']
        def page(self,json_object: dict) -> int:
            return json_object['Page']
    class filter(extract):
        def isText(self,json_object: dict) -> bool:
            """checks that :

            - object has text content, and

            - object does not belong to a table
            """
            
            if ("Text" in self.keys(json_object) and "Table" not in self.path(json_object)):
                return True
            return False
    class ToList(filter):
        def run(self,json_file: dict) -> list:
            """ Filter JSON dictionary into nested-list

            returns:
            
            [ (0) text category, 
            (1) text content, 
            (2) font weight, 
            (3) text size, 
            (4) text alignment, 
            (5) box bounds coordinates, 
            (6) page location ]
            """
            json_objects_list = []
            for json_object in json_file['elements']:
                if self.isText(json_object):
                    json_objects_list.append([
                        self.path(json_object), self.text(json_object), self.font_weight(json_object), self.text_size(json_object), self.text_alignment(json_object), self.bounds(json_object), self.page(json_object)
                    ])
            return json_objects_list    

class LIST_METHODS:
    class logic:
        def __init__(self) -> None:
            self.highLevelWords = ['chapter','section','appendix','annex','protocol','part']    
            self.lowLevelWords = ['article','footnote','l[','p']
            self.postBodyWords = ['annex','protocol','appendix','schedule']
        def isTopInPage(self, objects: list, json_object: list) -> bool:
            """For any JSON element, create list of all other elements in same page. 

            Then check if top position is greater than the other list elements.
            """
            page = [obj[5][3] for obj in objects if obj[6]==json_object[6]]            
            return all(x < json_object[5][3] for x in page[page.index(json_object[5][3])+1:])            
        def isTitleTag(self, objects: list, json_object: list) -> bool:
            if(("H" in json_object[0] or "Center" in json_object[5])
            and self.isTopInPage(objects,json_object)):  return True
            elif("H1" in json_object[0] or "Title" in json_object[0]): return True
            elif("H2" in json_object[0]): return True
            return False
        def isPreambleTag(self, objects: list, json_object: list) -> bool:
            if(all(highWord in json_object[1].lower() for highWord in self.highLevelWords)==False 
            and (json_object[2]==700 or self.isTopInPage(objects,json_object))
            and (not any(lowWord in json_object[0].lower() for lowWord in self.lowLevelWords))
            and "preamble" in json_object[1].lower()): return True
            return False        
        def isMainTag(self, objects: list, json_object: list) -> bool:
            if(any(json_object[1].lower().startswith(highWord) for highWord in self.highLevelWords)
            and (json_object[2]==700 or self.isTopInPage(objects,json_object))
            and (all(json_object[1].lower().startswith(lowWord) for lowWord in self.lowLevelWords)==False)
            and (all(json_object[0].lower().startswith(lowWord) for lowWord in self.lowLevelWords)==False)
            and "Center" in json_object[4]):                
                return True
            return False
        def isComplementTag(self, objects: list, json_object: list) -> bool:
            if(any(json_object[1].lower().startswith(postword) for postword in postBodyWords)
            and (json_object[2]==700 or self.isTopInPage(objects,json_object))
            and (not any(lowWord in json_object[0].lower() for lowWord in lowLevelWords))
            ): return True
            return False                    
        def isArticleTag(json_object: list) -> bool:
            if not any(lowtype in json_object[0].lower() for lowtype in lowType):
                if (json_object[1].lower().strip().startswith('article')):
                    x = json_object[1].lower().replace("article","").strip()
                    if any(x.startswith(str(num)) for num in under10): return True          
                elif any(json_object[1].lower().strip().startswith(str(num)) for num in under10) and json_object[2]==700: return True
            return False
        def hasSubsection(self, objects: list, avoid_tags: list) -> bool:
            for json_object in objects:
                if self.isMainTag(objects[objects.index(json_object):], json_object):
                        if any(tag in json_object[1].lower() for tag in avoid_tags): return False
                        elif not any(low in json_object[1].lower() for low in lowLevelWords): return True
            return False
    class categorize(logic):
        def whichMainTag(self,json_object: list) -> str:
            for highWord in self.highLevelWords:
                if highWord in json_object[1].lower().strip(): return highWord
            return ''
    class find(categorize):                    
        def section_number_name(self, next_object: list, this_object: list) -> list:
            notag = this_object[1].lower().replace(self.whichMainTag(this_object),"")
            if ":" in notag: 
                return [this_object[1].split(":")[0].strip(), this_object[1].split(":")[-1].strip()]
            elif ((next_object[2]==this_object[2] and next_object[4]==this_object[4])
            or (next_object[2]==this_object[2] and next_object[4]==this_object[4])
            or (next_object[3]==this_object[3] and "Center" in next_object[4])): 
                return [this_object[1].strip(),next_object[1].strip()]
            return [this_object[1].strip(),""]
        def article_number_name(self, next_object: list, this_object: list) -> list:
            notag = this_object[1].lower().replace("article","")
            if ":" in notag: 
                return [this_object[1].split(":")[0].strip(),this_object[1].split(":")[-1].strip()]
            elif("Center" in next_object[4] or next_object[2]==700):
                return [this_object[1].strip(),next_object[1].strip()]
            return [this_object[1].strip(),""]

        def this_section_tags(self, objects: list, search_tag: str) -> list:
            i = 0; num_names = []
            while(i < len(objects)-1):
                if self.isMainTag(objects, objects[i]) and objects[i][1].lower().startswith(search_tag):
                    num_name = self.section_number_name(objects[i+1],objects[i])
                    num_names.append(num_name)
                i+=1
            return num_names
        def subsection_in_section(self,objects: list, avoid_tags: list) -> str:
            for json_object in objects:
                if (self.isMainTag(objects,json_object)                    
                and not any(json_object[1].lower().startswith(tag) for tag in avoid_tags)):
                    return self.whichMainTag(json_object)
            return ""
    class index:
        def section_start(self, objects: list, num_name: list) -> int:
            if num_name[1]!="":
                for obj in objects:                                                            
                    if num_name[1] in obj[1]: return objects.index(obj)+1                    
            else:
                for obj in objects:
                    if obj[1].lower().startswith(num_name[0]): return objects.index(obj)+1
        def section_ends(self, objects: list, num_name: list) -> int:
            """
            Return the list index at which section ends.
            Inputs: (objects list) and the (number+name of the immediately next section tag)
            """
            for obj in objects:
                if obj[1].startswith(num_name[0]): return objects.index(obj)                  
        def preamble_ends(self, objects: list) -> int:
            for json_object in objects:
                if "have agreed as follows:" in json_object[1].lower(): return objects.index(json_object)
        def body_ends(self, objects: list) -> int:
            for json_object in objects:
                if "for the government of" in json_object[1].lower(): return objects.index(json_object)
        def map_section_indices(self, objects: list, num_names: list) -> list:
            """
            Return a list of ranges [init_ind, end_ind] for each section.
            """
            indices = []; i = 0            
            while (i < len(num_names)):
                if (i+1)>=len(num_names):
                    indices.append([self.section_start(objects,num_names[i]), len(objects)])
                else:
                    indices.append([self.section_start(objects,num_names[i]), self.section_ends(objects,num_names[i+1])])
                i+=1
            return indices    
    class content(find, index):
        def body_get_inner_ranges(self, objects: list, avoid_tags: list, index_map: list, index_position: int, base_index: int) -> list:
            search_tag = self.subsection_in_section(objects, avoid_tags)
            if search_tag != "":
                avoid_tags.append(search_tag)                
                num_names = self.this_section_tags(objects, search_tag)                
                indices = self.map_section_indices(objects, num_names)
                idx_position = index_position
                if "annex" in search_tag or "appendix" in search_tag: 
                    subsection_start_idx = [index_map[idx_position][0],base_index+indices[0][0]-2]
                    index_map.insert(idx_position,subsection_start_idx)
                    idx_position_temp = idx_position + 1
                    index_map.pop(idx_position_temp)
                    for idx in indices:
                        index_map.insert(idx_position_temp,[base_index+idx[0],base_index+idx[1]])
                        idx_position_temp+=1
                        index_map = self.get_inner_ranges(objects[idx[0]:idx[1]],avoid_tags,index_map,idx_position_temp-1,base_index+idx[0])                        
                else: 
                    index_map.pop(idx_position)
                    for idx in indices:                    
                        index_map.insert(idx_position,[base_index+idx[0],base_index+idx[1]])
                        idx_position+=1
                        index_map =  self.get_inner_ranges(objects[idx[0]:idx[1]],avoid_tags,index_map,idx_position-1,base_index+idx[0])
            return index_map        
        def body_get_ranges(self, objects: list) -> list:
            """
            Identify the first section in the body of the treaty
            """
            avoid_tags = []; indices = []   
            main_tag = self.subsection_in_section(objects,avoid_tags)            
            if main_tag!="":
                avoid_tags.append(main_tag)
                num_names = self.this_section_tags(objects,main_tag)
                indices =  self.map_section_indices(objects,num_names); j=0
                #while (j<len(indices))
                for idx in indices:                                    
                    indices =  self.get_inner_ranges(
                     objects[idx[0]:idx[1]],avoid_tags,indices,indices.index(idx),idx[0]   
                    )
            return indices        
    class structure(find,index):
        def body_inner_schema(self, objects: list, num_name: list, num_names: list, avoid_tags: list, index_position: int) -> list:
            search_tag = self.subsection_in_section(objects, avoid_tags) 
            idx_position = index_position           
            if search_tag != "":
                idx_position = (index_position+1 if "annex" in search_tag or "appendix" in search_tag else index_position)
                avoid_tags.append(search_tag)
                num_names_inner = self.this_section_tags(objects, search_tag)
                indices = self.map_section_indices(objects, num_names_inner)
                if "annex" in search_tag or "appendix" in search_tag: num_names.append(idx_position)
                for num_name_inner in num_names_inner:
                    num_names.insert(
                        idx_position,
                        [num_name[0]+". "+num_name_inner[0],num_name[1]+". "+num_name_inner[1]]
                    )
                    idx_position+=1
                    num_names_inner = self.inner_schema(
                        objects[indices[num_names_inner.index(num_name_inner)][0]:indices[num_names_inner.index(num_name_inner)][1]],
                        num_name_inner,
                        num_names_inner,
                        avoid_tags,
                        idx_position
                    )
            return num_names
        def body_main_schema(self, objects: list) -> list:
            avoid_tags = []; num_names = []
            main_tag = self.subsection_in_section(objects, avoid_tags)
            if main_tag != "":
                avoid_tags.append(main_tag); num_names = self.this_section_tags(objects, main_tag)
                indices = self.map_section_indices(objects, num_names); len_start=len(num_names)
                for num_name in num_names:         
                    if len(indices) == num_names.index(num_name): break
                    num_names = self.inner_schema(
                        objects[indices[num_names.index(num_name)][0]:indices[num_names.index(num_name)][1]],
                        num_names[num_names.index(num_name)+(len(num_names)-len_start)], 
                        num_names, 
                        avoid_tags, 
                        num_names.index(num_name)+(len(num_names)-len_start)
                    )                    
            return num_names
        def complement_main_schema(self, objects: list) -> list:
            num_names = []; i = 0
            while (i < len(objects)-1):
                if self.isMainTag(objects,objects[i]):
                    num_name = self.section_number_name(objects[i+1],objects[i])
                    num_names.append(num_name)
                i+=1
            return num_names
                    
        def section_preamble_get(self, objects: list) -> list:
            return objects[:self.preamble_ends(objects)]            
        def section_body_get(self, objects: list):
            return objects[self.preamble_ends(objects)+1:self.body_ends(objects)]
        def section_complement_get(self, objects: list) -> list:
            return objects[self.body_ends(objects):]
        def subsection_annex_get(self, complement:list) -> list:
            indices = []; num_name = []
            for json_object in complement:
                if self.isMainTag(complement, json_object):
                    if len(indices)==2: break
                    if self.whichMainTag(json_object)=="annex":
                        num_name = self.article_number_name(complement[complement.index(json_object)+1],json_object)
                        indices.append(complement.index(json_object)+1)
                    else:
                        if len(indices)==1:
                            indices.append(complement.index(json_object))               
            return [num_name,indices]
        def subsection_protocol_get(self, complement: list) -> list:
            indices = []; num_name = []
            for json_object in complement:
                if self.isMainTag(complement, json_object) and any(json_object[1].lower().startswith(postword) for postword in self.postBodyWords):
                    if len(indices)==2: break
                    elif len(indices)==0:
                        if self.whichMainTag(json_object)=="protocol":
                            num_name = self.section_number_name(
                                complement[complement.index(json_object)+1],
                                complement[complement.index(json_object)]
                            )
                            indices.append(complement.index(json_object))
                    else:
                        if self.whichMainTag(json_object)!="annex":
                            indices.append(complement.index(json_object))
            if len(indices)==1: indices.append(len(complement))
            else: return [num_name,indices]
            return [num_name,indices]
        def subsection_appendix_get(self, complement: list) -> list:
            indices = []; num_name = []
            for json_object in complement:
                if self.isMainTag(complement, json_object) and any(json_object[1].lower().startswith(postword) for postword in self.postBodyWords):
                    if len(indices)==2: break
                    elif len(indices)==0:
                        if self.whichMainTag(json_object)=="appendix":
                            num_name = self.section_number_name(
                                complement[complement.index(json_object)+1],
                                complement[complement.index(json_object)]
                            )
                            indices.append(complement.index(json_object))
                    else:
                        if self.whichMainTag(json_object)!="annex":
                            indices.append(complement.index(json_object))
            if len(indices)==1: indices.append(len(complement))
            else: return [num_name,indices]
            return [num_name,indices]
            
            pass
    class organize(content, structure):
        def body_into_articles(self,body):            
            body_structure = self.body_main_schema(body)
            body_content = self.body_get_ranges(body)
            for json_object in body:
                if self.isArticleTag(json_object):
                    num_name = self.article_number_name(body[body.index(json_object)+1],json_object)
                    
filepath = "demo_files/pta_446.json"
with open(filepath,'r') as f:
    file = json.load(f)
    json_to_list = DICTIONARY_METHODS.ToList()
    objects_list = json_to_list.run(file)
    functions = LIST_METHODS()
    body = functions.structure().section_body_get(objects_list)
    x = functions.organize().body_into_articles(body)
    #print(complement[return_list[0]:return_list[1]])
    #for y in return_list: print(complement[y[0]:y[1]], end="\n\n")



       
#----------------------------------------------------------------------------------------
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