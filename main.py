from modules_ import *

filepath = "demo_files/pta_192.json"
with open(filepath,'r') as f:
    file = json.load(f)
    #x = test(file)
    #for y in x: print(y,end="\n\n")
    print(file)

"""

def main(section_tags, objects_list):
    foundNext = False; ind = 0
    while not foundNext:
        ind+=1
        if ind>=len(objects_list): 
            foundNext = True
            break; 
        else: 
            if objects_list[ind][2]==700:                
                if parseJSON.logical.isSubsectionTag(objects_list[ind],section_tags):
                    print(objects_list[ind])                    
                



with open("demo_files/pta_192.json",'r') as f:
    file = json.load(f)   
    #x = parseJSON.structure.hierarchySchema.get(file)    
    #for y in x: print(y,end="\n\n")        
    objects_list = parseJSON.structure.byObject(file); ind=0
    section_tag = 'chapter'; section_tags = [section_tag] # the section tags found so far
    while(ind < len(objects_list)): 
        if(parseJSON.logical.isMainTag(objects_list[ind:],objects_list[ind])
        and section_tag in objects_list[ind][1].lower()):            
            if parseJSON.logical.hasSubsection(objects_list[ind+1:], section_tags):                 
                print(objects_list[ind][1])
                main(section_tags,objects_list[ind:])                
        ind+=1


"""    