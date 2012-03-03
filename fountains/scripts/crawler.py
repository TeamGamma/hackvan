import sys, string, math, time, socket
import flickrapi
from django.utils.encoding import smart_str, smart_unicode
from fountain import fountain

class crawler:
    def __init__(self, api_key_):
        self.api_key = api_key_ #hard code your api key
        self.flickr = flickrapi.FlickrAPI(self.api_key)
        #a list for fountains information
        self.fountains = []
        
    def search(self, text_search):
        try:
            outs_phs = self.flickr.photos_search(text=text_search)
            all_photos = outs_phs.find('photos')
            photos = all_photos.findall('photo')    #list of all photos
        except KeyboardInterrupt:
            print('Keyboard exception while querying your requested photos, exiting\n')
            raise
        except:
            print sys.exc_info()[0]
            print ('Exception encountered while querying your requested photos\n')
        else:            
            #let's print all photo sets belong to this user
            for photo in photos:
                lat_ = 'NA'
                lng_ = 'NA'
                info = 'NA'
                date = 'NA'
                taken_time ='NA'
                title = 'fountain'
                
                fount_id = photo.attrib['id']
                fount_title = photo.attrib['title']
                #let's extract the location of each photo
                try:
                    fount_loc = self.flickr.photos_geo_getLocation(photo_id = fount_id)
                except KeyboardInterrupt:
                    print('Keyboard exception while querying for a fountain, exiting\n')
                    raise
                except:
                    print sys.exc_info()[0]
                    print ('Exception encountered while querying a fountain location\n')
                else:
                    loc_ = fount_loc.find('photo').find('location')
                    lat_ = loc_.attrib['latitude']
                    lng_ = loc_.attrib['longitude']
                try:
                    fount_info = self.flickr.photos_getInfo(photo_id = fount_id)
                except KeyboardInterrupt:
                    print('Keyboard exception while querying for a fountain, exiting\n')
                    raise
                except:
                    print sys.exc_info()[0]
                    print ('Exception encountered while querying a fountain location\n')
                else:                
                    info = fount_info.find('photo')
                    date = info.find('dates')
                    taken_time = date.attrib['taken']
                    title = info.find('title').text
                    print info
                fount_ = fountain(lat_, lng_, taken_time, fount_id, title)
                self.fountains.append(fount_)

    def write_fountains(self):
        print "No of fountain photos: ", len(self.fountains)
        file_name = '/Users/kazemjahanbakhsh/Downloads/Hackathon/fountains.dat'
        f_ = open(file_name, 'w')
        for fount_ in self.fountains:              
            entry_ = "%s,%s,%s,%s,\"%s\"\n" % (fount_.ph_id, fount_.latit, fount_.longit, fount_.time_, smart_str(fount_.title))
            f_.write(entry_)
                
        f_.close()