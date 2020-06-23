import sys
import os
import json
import fitz
     
        
def conv(path_to_file:str)->None:
    folder, filename = os.path.split(path_to_file)
    if not filename.endswith('.pdf'): 
        print(json.dumps({'status': 'failed',
                          'msg': 'Wrong file extension'}))
        
    elif not os.path.exists(path_to_file):
        print(json.dumps({'status': 'failed',
                          'msg': "File doesn't exists"}))
        
    else:
        doc = fitz.open(path_to_file)  
        pages = doc.pageCount
        pix_files = []
    
        for page_num in range(pages):
            page = doc.loadPage(page_num)
            pix = page.getPixmap()
            filename = filename.split('.')[0]
            pix_filename = "{}_{}.png".format(filename,page_num)
            write_path = os.path.join(folder, pix_filename)
            pix_files.append(write_path)
            pix.writeImage(write_path)
        
        for pix_file in pix_files:
            if not os.path.exists(pix_file):
                print(json.dumps({'status': 'failed',
                                  'msg': 'Images not created'}))
                break           
        else:
            print(json.dumps({'status': 'success'}))
        
        
if __name__ == "__main__":
    try:
        filepath = sys.argv[1]
        conv(filepath)    
    except (IndexError, NameError):
        print(json.dumps({'status': 'failed', 
                          'msg': 'No filename provided'}))
    except (RuntimeError) as error:
        if 'Permission denied' in error.args[0]:
            print(json.dumps({'status': 'failed', 
                              'msg': 'Permission denied'}))
        else: 
            print(json.dumps({'status': 'failed', 
                              'msg': error.args}))
