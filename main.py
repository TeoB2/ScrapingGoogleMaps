from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time


restaurantList = {}
restaurantDict = {}


class WebDriver:
    location_data = {}


    flagOpenCloseTimeOtherWindow = False

    def __init__(self):
        self.PATH = "./chromedriver"
        self.options = Options()
        # self.options.binary_location = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"
        #self.options.add_argument("--headless")
        #self.options.add_argument("--disable-gpu")

        self.driver = webdriver.Chrome(self.PATH, options=self.options)
        #self.driver = webdriver.Chrome(self.PATH)

        self.location_data["name"] = "NA"
        self.location_data["rating"] = "NA"
        self.location_data["reviews_count"] = "NA"
        self.location_data["location"] = "NA"
        self.location_data["contact"] = "NA"
        self.location_data["website"] = "NA"
        self.location_data["Time"] = {"Lunedì": "NA", "Martedì": "NA", "Mercoledì": "NA", "Giovedì": "NA",
                                      "Venerdì": "NA", "Sabato": "NA", "Domenica": "NA"}
        self.location_data["Reviews"] = []
        #self.location_data["Popular Times"] = {"Lunedì": [], "Martedì": [], "Mercoledì": [], "Giovedì": [],
        #                                       "Venerdì": [], "Sabato": [], "Domenica": []}

        dayEnglish = {0: "Sunday", 1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday"}
        dayItalian = {0: "Domenica", 1: "Lunedì", 2: "Martedì", 3: "Mercoledì", 4: "Giovedì", 5: "Venerdì", 6: "Sabato"}

        self.flagOpenCloseTimeOtherWindow = False


    #accetta i cookie prima di guardare la mappa
    def clickAllowCookie(self):

        #scrolla la pagina fino al bottom
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        try:
            #abbiamo due bottoni con la classe nCP5yc, devo selezionare sempre l'ultimo

            self.driver.find_elements_by_css_selector('button.nCP5yc')[-1].click()
        except:
            print("Errore durante il click sul bottone Accetta cookie")

            self.driver.quit()
            return False

        return True


    #preme sul pulsante per mostrare tutti i ristoranti vicino alle coordinate inserite
    def clickButtonRestaurant(self):

        try:
            #abbiamo cinque bottoni con la classe NIyLF-haAclf, devo selezionare sempre il secondo

            self.driver.find_elements_by_css_selector('button.NIyLF-haAclf')[2].click()
        except:
            print("Errore durante il click sul bottone dei ristoranti del luogo selezionato")

            self.driver.quit()
            return False

        return True


    #restituisce la lista dei ristoranti vicino alle coordinate inserite
    def getRestaurantList(self):

        try:

            global restaurantList
            restaurantList = self.driver.find_elements_by_css_selector('a.a4gq8e-aVTXAb-haAclf-jRmmHf-hSRGPd')

        except:
            print("Errore durante il recupero dei ristoranti nei paraggi")

            self.driver.quit()
            return False

        return True


    #apre-chiude il div contenente gli orari del ristorante
    def clickOpenCloseTime(self):

        try:
            #controllo se gli orari sono in una nuova finestra o se si apre una tendina
            if len(self.driver.find_elements_by_css_selector('div.hH0dDd')):

                #apro tendina
                self.driver.find_element_by_css_selector('div.hH0dDd').click()

            else:

                #apro nuova finestra e setto un flag
                self.driver.find_elements_by_css_selector('button.CsEnBe')[1].click()
                self.flagOpenCloseTimeOtherWindow = True

        except:
            print("Errore durante l'apertura degli orari del ristorante")

            self.driver.quit()
            return False

        return True


    #visualizzo tutte le recensioni del ristorante
    def clickAllReviewsButton(self):
        try:
            self.driver.find_elements_by_css_selector("button.Yr7JMd-pane-hSRGPd")[0].click()
        except:
            print("Impossibile aprire le recensioni del ristorante")

            self.driver.quit()
            return False

        return True


    #restuisce il nome del ristorante
    def getNameRestaurant(self):

        try:

            name = self.driver.find_element_by_css_selector("h1.x3AX1-LfntMc-header-title-title")

        except:

            print("Impossibile trovare il nome del ristorante")
            return False

        return name.text


    #restuisce il valore medio delle recensioni del ristorante
    def getAvgRatingRestaurant(self):

        try:

            avgRating = self.driver.find_element_by_class_name("aMPvhf-fI6EEc-KVuj8d")

        except:

            print("Impossibile trovare la media delle recensioni del ristorante")
            return False

        return avgRating.text


    #restuisce il numero delle recensioni del ristorante
    def getTotalReviewRestaurant(self):

        try:

            totalReviews = self.driver.find_elements_by_css_selector("button.Yr7JMd-pane-hSRGPd")[0]

        except:

            print("Impossibile trovare il numero delle recensioni del ristorante")
            return False

        return totalReviews.text[1:-1]


    #restuisce l'indirizzo del ristorante
    def getLocationRestaurant(self):

        try:

            address = self.driver.find_elements_by_css_selector("div.QSFF4-text")[0]

        except:

            print("Impossibile trovare l'indirizzo del ristorante")
            return False

        return address.text


    #restuisce il numero di telefono del ristorante
    def getPhoneNumberRestaurant(self):

        try:

            phoneNumber = self.driver.find_elements_by_css_selector("div.QSFF4-text")[-1]

        except:

            print("Impossibile trovare il numero di telefono del ristorante")
            return False

        return phoneNumber.text

    #restuisce il sito internet del ristorante
    def getWebSiteRestaurant(self):

        try:

            website = self.driver.find_elements_by_css_selector("div.QSFF4-text")[-2]

        except:

            print("Impossibile trovare il sito internet del ristorante")
            return False

        return website.text


    #prende gli orari relativi ai giorni della settimana di apertura-chiusura del ristorante
    def getLocationOpenCloseTime(self):

        time = {}

        try:

            days = self.driver.find_elements_by_css_selector("th.y0skZc-header")
            times = self.driver.find_elements_by_css_selector("ul.y0skZc-t0oSud")

            #ciclo i giorni e gli orari
            day = [a.text.title() for a in days]
            open_close_time = [a.text for a in times]

            for i, j in zip(day, open_close_time):

                if len(i) <= 0 or len(j) <= 0:
                    continue

                time[i] = j

        except:
            print("Errore durante il prelievo degli orari del ristorante")

            self.driver.quit()
            return False

        #se gli orari sono in un'altra finestra torno indietro
        if self.flagOpenCloseTimeOtherWindow:
            self.driver.find_element_by_css_selector('button.VfPpkd-icon-LgbsSe').click()
            self.flagOpenCloseTimeOtherWindow = False
            self.sleep(5)

        return time

    def get_popular_times(self):
        try:
            a = self.driver.find_elements_by_class_name("O9Q0Ff-NmME3c-Utye1-Fq92x")
            l = {"Sunday": [], "Monday": [], "Tuesday": [], "Wednesday": [], "Thursday": [], "Friday": [],
                 "Saturday": []}
            count = 0

            for i in a:
                b = i.find_elements_by_class_name("section-popular-times-bar")
                for j in b:
                    x = j.get_attribute("aria-label")
                    l[self.dayEnglish[count]].append(x)
                count = count + 1

            for i, j in l.items():
                self.location_data["Popular Times"][i] = j
        except:
            pass


    #scrolla il div con la lista dei ristoranti o delle recensioni
    def scrollThePage(self, review = False):

        try:
            limitCount = 5
            counter = 0

            while (counter < limitCount):

                if review:
                    scrollable_div = self.driver.find_element_by_css_selector('div.section-scrollbox')
                else:
                    scrollable_div = self.driver.find_elements_by_css_selector('div.section-scrollbox')[1]

                try:
                    self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
                except:
                    print("Errore durante la scroll numero " + str(counter))
                    pass

                self.sleep(3)
                counter = counter + 1
        except:
            print("Errore durante la scroll")
            self.driver.quit()

            return False

        return True


    #espande tutte le recensioni lunghe
    def expandAllReviews(self):

        try:
            element = self.driver.find_elements_by_class_name("ODSEW-KoToPc-ShBeI")
            for i in element:
                if not i:
                    continue

                i.click()
        except:
            print("Impossibile espandere tutte le recensioni")

            return False

        return True


    #scraping delle recensioni
    def getReviewsData(self):

        reviews = []

        try:
            review_names = self.driver.find_elements_by_class_name("ODSEW-ShBeI-title")
            review_text = self.driver.find_elements_by_class_name("ODSEW-ShBeI-text")
            review_dates = self.driver.find_elements_by_class_name("ODSEW-ShBeI-RgZmSc-date")
            review_stars = self.driver.find_elements_by_class_name("ODSEW-ShBeI-H1e3jb")

            review_stars_final = []

            for i in review_stars:
                review_stars_final.append(i.get_attribute("aria-label"))

            review_names_list = [a.text for a in review_names]
            review_text_list = [a.text for a in review_text]
            review_dates_list = [a.text for a in review_dates]
            review_stars_list = [a for a in review_stars_final]

            for (a, b, c, d) in zip(review_names_list, review_text_list, review_dates_list, review_stars_list):
                reviews.append({"name": a, "review": b, "date": c, "rating": d})

        except Exception as e:
            print("Errore durante il recupero delle recensioni del ristorante")

            return False

        self.driver.find_element_by_css_selector('button.VfPpkd-icon-LgbsSe').click()

        return reviews


    #metodo per eseguire una sleep
    def sleep(self, second = 1):

        if (second is None or second < 0) and isinstance(second, float):
            return False

        time.sleep(second)

        return True


    def scrape(self, url):

        try:
            self.driver.get(url)

        except Exception as e:
            self.driver.quit()
            return (self.location_data)

        self.sleep(0.1)

        #click per accettare i cookie
        clickAllowCookie = self.clickAllowCookie()
        if clickAllowCookie == False:
            return (self.location_data)


        self.sleep(5)


        #click sul bottone per la ricerca dei ristoranti
        clickButtonRestaurant = self.clickButtonRestaurant()
        if clickButtonRestaurant == False:
            return (self.location_data)


        self.sleep(5)


        #restituisce la lista dei ristoranti nei paraggi
        getRestaurantList = self.getRestaurantList()
        if getRestaurantList == False:
            return (self.location_data)


        counter = 0

        #ciclo i risoranti nei paraggi
        for restaurant in restaurantList:

            if not restaurant:
                continue

            #scrolla il div con la lista dei ristoranti
            self.scrollThePage(False)

            self.sleep(5)
            #faccio il click sul ristorante
            self.driver.find_elements_by_css_selector('a.a4gq8e-aVTXAb-haAclf-jRmmHf-hSRGPd')[counter].click()

            self.sleep(5)

            #prende il nome del ristorante
            getNameRestaurant = self.getNameRestaurant()
            if getNameRestaurant == False:
                continue


            #prende le recensioni medie del ristorante
            getAvgRatingRestaurant = self.getAvgRatingRestaurant()
            if getAvgRatingRestaurant == False:
                continue


            #prende il numero di recensioni del ristorante
            getTotalReviewRestaurant = self.getTotalReviewRestaurant()
            if getTotalReviewRestaurant == False:
                continue


            #prende l'indirizzo del ristorante
            getLocationRestaurant = self.getLocationRestaurant()
            if getLocationRestaurant == False:
                continue


            #prende il numero di telefono del ristorante
            getPhoneNumberRestaurant = self.getPhoneNumberRestaurant()
            if getPhoneNumberRestaurant == False:
                continue


            #prende il sito internet del ristorante
            getWebSiteRestaurant = self.getWebSiteRestaurant()
            if getWebSiteRestaurant == False:
                continue


            self.sleep(5)


            #apro gli orari del ristorante
            clickOpenCloseTime = self.clickOpenCloseTime()
            if clickOpenCloseTime == False:
                continue


            self.sleep(5)


            #prendo i giorni e gli orari di apertura-chiusura del ristorante
            getLocationOpenCloseTime = self.getLocationOpenCloseTime()
            if getLocationOpenCloseTime == False:
                continue


            self.sleep(5)


            #visualizzo tutte le recensioni del ristorante
            clickAllReviewsButton  = self.clickAllReviewsButton()
            if clickAllReviewsButton == False:
                continue


            self.sleep(5)

            #scrolla il div con le recensioni di un ristorante
            self.scrollThePage(True)

            #espande tutte le recensioni lunghe
            expandAllReviews = self.expandAllReviews()
            if expandAllReviews == False:
                continue


            #scrap delle recensioni del ristorante
            getReviewsData = self.getReviewsData()
            if getReviewsData == False:
                continue


            #assegno a location data quello rilevato nello scraping
            self.location_data["Time"] = getLocationOpenCloseTime
            self.location_data["name"] = getNameRestaurant
            self.location_data["rating"] = getAvgRatingRestaurant
            self.location_data["reviews_count"] = getTotalReviewRestaurant
            self.location_data["location"] = getLocationRestaurant
            self.location_data["contact"] = getPhoneNumberRestaurant
            self.location_data["website"] = getWebSiteRestaurant
            self.location_data["Reviews"] = getReviewsData


            #metto nel dict restaurantDict tutti i dati prelevati del ristorante
            restaurantDict[counter] = self.location_data

            counter = counter + 1


            self.driver.find_element_by_css_selector('button.xo8g7').click()


            self.sleep(5)


        self.driver.quit()

        return (restaurantDict)


url = "https://www.google.it/maps/@45.0244498,7.6355183,17z"
x = WebDriver()
print(x.scrape(url))