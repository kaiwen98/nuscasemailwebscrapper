import scrapy
import re

if __name__ == "__main__":
    print("hi")
    print(not(re.match("PA_[A-Z]+@pa.gov.sg", "PA_PASIRRISELIASCC@pa.gov.sg") is None))



class CCEmailSpider(scrapy.Spider):
    name = "nuscas"
    email_list = []
    email_regex_str = "PA_[A-Z]+@pa.gov.sg"
    output_email_file = 'emails.txt'

    def is_valid_email(self, email):
        return not(re.match("[A-Za-z_]+@pa.gov.sg", email) is None)

    def parse(self, response):
        sel = scrapy.Selector(response)
        print(response.url)
        self.start_requests()
        with open(f"marsiling.html", "wb") as f:
            f.write(response.body)
        
        entry = (sel.xpath("//h2[contains(., 'Contact Information')]/following-sibling::p/a/@href").extract())[0][7:]
        print(entry)
        if (self.is_valid_email(str(entry))):
            self.email_list.append(entry)

    def start_requests(self):
        urls = self.generate_websites()

        # Set the headers here. The important part is "application/json"
        headers =  {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36'
            }
    
        for url in urls:
            yield scrapy.Request(url = url, headers=headers, callback = self.parse)

        self.output_email_list()

    def output_email_list(self):
        self.email_list = list(dict.fromkeys(self.email_list))

        print(self.email_list)
        
        for entry in self.email_list:
            with open(self.output_email_file, 'a') as f:
                f.write(str(entry) + "; \n")


    def generate_websites(self):
        url = 'https://www.pa.gov.sg/our-network/community-clubs/locate-cc/detail/'
        cc_names = ['Braddell Heights Community Club', 'Marsiling Community Club', 'Ci Yuan Community Centre', 'Kolam Ayer Community Club', 'Bukit Timah Community Club', 'Punggol 21 Community Club', 'Fuchun Community Club', 'Tanglin Community Club', 'Hong Kah North Community Club', 'Anchorvale Community Club', 'Pasir Ris Elias Community Club', 'Bishan Community Club', 'Sengkang Community Club', 'Tanjong Pagar Community Club', 'The Frontier Community Club', 'Queenstown Community Centre', 'Siglap South Community Centre', 'Woodlands Galaxy Community Club', 'Leng Kee Community Club', 'Yuhua Community Club', 'Rivervale Community Centre', 'Jurong Spring Community Club', 'Bukit Batok Community Club', 'Our Tampines Hub', 'Nee Soon South Community Club', 'Toa Payoh South Community Club', 'Keat Hong Community Club', 'Teck Ghee Community Club', 'Fengshan Community Club', 'Kim Seng Community Centre', 'Jalan Besar Community Club', 'Telok Blangah Community Club', 'Sembawang Community Club', 'Cairnhill Community Club', 'Nee Soon Central Community Club', 'Thomson Community Club', 'Nee Soon East Community Club', 'Pek Kio Community Centre', 'Mountbatten Community Club', 'Potong Pasir Community Club', 'Zhenghua Community Club', 'Whampoa Community Club', 'Toa Payoh Central Community Club', 'Ayer Rajah Community Club', 'Bukit Merah Community Centre', 'Geylang West Community Club', 'Punggol Community Club', 'Toa Payoh East Community Club', 'Tampines Changkat Community Club', 'Cheng San Community Club', 'Gek Poh Ville Community Club', 'Kampong Chai Chee Community Club at Heartbeat@Bedok', 'Bukit Panjang Community Club', 'Punggol Park Community Centre', 'Geylang Serai Community Club', 'Aljunied Community Centre', 'Tampines West Community Club', 'Tampines Central Community Club @ Our Tampines Hub', 'Chua Chu Kang Community Club', 'Senja-Cashew Community Club', 'Eunos Community Club', 'Jurong Green Community Club', 'Hillview Community Club', 'Bukit Batok East Community Club', 'Paya Lebar Kovan Community Club', 'Taman Jurong Community Club', 'West Coast Community Centre', 'Limbang CC', 'Hwi Yoh Community Centre', 'Buona Vista Community Club', 'Tampines North Community Club', 'Kampong Glam Community Club', 'Kaki Bukit Community Centre', 'Kebun Baru Community Club', 'Joo Chiat Community Club', 'Boon Lay Community Club', 'Kallang Community Club', 'Ulu Pandan Community Club', 'Henderson Community Club', 'The Serangoon Community Club', 'Chong Pang Community Club', 'Tiong Bahru Community Centre', 'Nee Soon Spring Community Centre', 'Dover Community Centre', 'Canberra Community Club', 'Clementi Community Centre', 'Punggol Vista Community Centre', 'ACE The Place Community Club', 'Marine Parade Community Club', 'Woodgrove Community Centre', 'Toa Payoh West Community Club', 'MacPherson Community Club', 'Changi Simei Community Club', 'Radin Mas Community Club', 'Katong Community Centre', 'Yio Chu Kang Community Club', 'Bedok Community Centre', 'Kampong Kembangan Community Club', 'Yew Tee Community Club', 'Pasir Ris East Community Club', 'Woodlands Community Club', 'Siglap Community Centre', 'Ang Mo Kio Community Centre', 'Nanyang Community Club', 'Tampines East Community Club', 'Hougang Community Club', 'Marymount Community Club', 'Kreta Ayer Community Club', 'Kampong Ubi Community Centre']

        print("size of list: ", len(cc_names))
        i = 0
        for cc_name in cc_names:
            cc_names[i] = url + cc_name.replace('@ ', '').replace('@', " ").replace(' ', '-')
            i += 1
        
        return cc_names
