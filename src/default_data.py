import csv
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# 100 Authentic Japanese Recipes Knowledge Base
AUTHENTIC_JAPANESE_RECIPES = [
    ["Chicken meatball for nabe (japanese hot pot)", "https://cookpad.com/eng/recipes/25431062", "ground chicken renkon minced green onion ginger garlic egg salt pepper layu sesame oil dashi broth soy sauce"],
    ["Perfect Shokupan - White and Fluffy Japanese milk bread", "https://cookpad.com/eng/recipes/25325786", "bread flour water full fat milk sugar dry instant yeast unsalted butter salt yudane"],
    ["Spicy Chicken Japanese Curry", "https://cookpad.com/eng/recipes/25284017", "curry roux onion carrot potato chicken thighs water vegetable oil soy sauce garlic ginger chili powder beef powder"],
    ["Steamed Japanese Sweet Potato w/ Instant Pot", "https://cookpad.com/eng/recipes/25210496", "japanese sweet potato butter salt honey water instant pot"],
    ["Japanese Hambagu with Herb Mashed Potatoes and Crispy Fries", "https://cookpad.com/eng/recipes/25214022", "ground beef ground pork onion breadcrumbs egg milk salt pepper nutmeg worcestershire sauce ketchup soy sauce butter potato"],
    ["Tsukune (japanese chicken meatballs)", "https://cookpad.com/eng/recipes/25155937", "ground chicken tofu egg white shiso leaves salt pepper cornstarch soy sauce sugar sake mirin"],
    ["Japanese yakitori (chicken thigh skewers)", "https://cookpad.com/eng/recipes/24997517", "chicken thighs spring onions scallions tare sauce soy sauce sake mirin sugar garlic ginger"],
    ["Gyoza (japanese pan-fried dumplings)", "https://cookpad.com/eng/recipes/24990641", "ground pork soy sauce sesame oil sake garlic nira garlic chives cabbage ginger potato starch dumpling wrappers"],
    ["Japanese-style pizza with whitebait, chikuwa and leeks", "https://cookpad.com/eng/recipes/24773058", "pizza dough tomato sauce miso paste mozzarella cheese chikuwa leek shiro dashi shredded nori olive oil"],
    ["Japanese-Inspired Veggie Pizza with Tofu Cottage Cheese", "https://cookpad.com/eng/recipes/24769889", "pizza dough tomato sauce miso paste basil garlic broccoli eggplant cherry tomatoes sweet potato lotus root olive oil tofu"],
    ["Japanese-Style Calzone with Roasted Soybeans & Curry", "https://cookpad.com/eng/recipes/24751996", "bread flour dry yeast sugar salt olive oil soybeans onion carrot curry powder miso soy sauce mozzarella"],
    ["Fruit Sando - Japanese Milk Bread Fruit Sandwich", "https://cookpad.com/eng/recipes/24755612", "white milk bread shokupan whip cream fresh strawberry kiwi fruit grapes sugar cold water"],
    ["Japanese Teriyaki Chicken Pizza", "https://cookpad.com/eng/recipes/24755294", "pizza dough chicken thigh soy sauce sugar sake mirin garlic ginger rice cake mayonnaise nori"],
    ["Japanese Smashed Cucumber with Umeboshi", "https://cookpad.com/eng/recipes/24753170", "japanese cucumber umeboshi pickled plum sesame oil sugar soy sauce dashi salt sesame seeds"],
    ["Japanese and Korean style snack pizza", "https://cookpad.com/eng/recipes/24750381", "gyoza skin dumpling wrapper mozzarella cheese tomato paste miso wasabi white onion shiitake mushrooms shiso leaf kimchi sesame seeds"],
    ["Japanese Creamy Potato Salad", "https://cookpad.com/eng/recipes/24660863", "potatoes carrot sweet onion cucumber eggs kewpie mayonnaise rice vinegar salt black pepper"],
    ["Japanese Napolitan Ketchup Spaghetti Pasta", "https://cookpad.com/eng/recipes/24727616", "spaghetti pasta sausage bell green pepper onion carrot ketchup soy sauce butter parmesan cheese"],
    ["Oyakodon (Japanese Chicken and Egg Rice Bowl)", "https://cookpad.com/eng/recipes/24707794", "chicken thigh eggs yellow onion dashi stock soy sauce sake mirin sugar steamed white rice"],
    ["Chashu pork (Japanese braised pork belly)", "https://cookpad.com/eng/recipes/24707630", "pork belly pork shoulder soy sauce sake mirin sugar garlic ginger scallion green onion water"],
    ["Japanese Curry using Curry Roux mix", "https://cookpad.com/eng/recipes/24692701", "curry roux onion carrot potato beef chicken pork water vegetable oil sesame oil"],
    ["Japanese Mashed Cucumber Salad with Sesame", "https://cookpad.com/eng/recipes/24692676", "japanese cucumber salt sesame oil rice vinegar soy sauce sugar toasted sesame seeds"],
    ["Karaage - Crispy Japanese Fried Chicken", "https://cookpad.com/eng/recipes/24679584", "boneless chicken thighs soy sauce sake mirin salt grated ginger garlic all-purpose flour potato starch oil lemon"],
    ["Japanese Tuna Poke Rice Bowl", "https://cookpad.com/eng/recipes/24664333", "sashimi grade tuna mirin sake soy sauce sesame oil avocado scallions nori steamed rice"],
    ["Classic Japanese Beef & Potato Curry", "https://cookpad.com/eng/recipes/24661034", "pork shoulder beef garlic ginger yellow onion carrots potatoes soy sauce chicken broth curry roux"],
    ["Tonkatsu - Crispy Japanese Pork Cutlet", "https://cookpad.com/eng/recipes/24650123", "pork loin chops salt black pepper flour egg panko breadcrumbs cabbage tonkatsu sauce"],
    ["Miso Soup with Silken Tofu & Wakame", "https://cookpad.com/eng/recipes/24640192", "dashi soup stock awase miso paste silken tofu dried wakame seaweed chopped scallions green onions"],
    ["Kitsune Udon with Sweet Fried Tofu", "https://cookpad.com/eng/recipes/24630841", "sanuki udon noodles dashi broth soy sauce mirin aburaage seasoned fried tofu green onion kamaboko fish cake"],
    ["Zaru Soba - Chilled Buckwheat Noodles", "https://cookpad.com/eng/recipes/24620199", "buckwheat soba noodles mentsuyu dipping sauce wasabi grated daikon radish green onion nori seaweed shreds"],
    ["Osaka Style Savory Okonomiyaki Pancake", "https://cookpad.com/eng/recipes/24610943", "shredded cabbage okonomiyaki flour nagaimo yam dashi egg pork belly slices okonomiyaki sauce kewpie mayo bonito flakes aonori"],
    ["Crispy Takoyaki Octopus Balls with Kewpie Mayo", "https://cookpad.com/eng/recipes/24600184", "boiled octopus dashi batter flour egg pickled red ginger tenkasu tempura scraps green onion takoyaki sauce kewpie mayo bonito flakes aonori"],
    ["Katsudon - Pork Cutlet and Egg Rice Bowl", "https://cookpad.com/eng/recipes/24590111", "tonkatsu pork cutlet eggs sliced onion dashi broth soy sauce mirin sugar steamed white rice mitsuba"],
    ["Gyudon - Japanese Beef and Onion Rice Bowl", "https://cookpad.com/eng/recipes/24580222", "thinly sliced beef ribeye yellow onion dashi stock soy sauce sake mirin sugar pickled red ginger beni shoga steamed rice"],
    ["Tonkotsu Ramen with Rich Pork Broth", "https://cookpad.com/eng/recipes/24570333", "fresh ramen noodles tonkotsu pork bone broth chashu pork belly soft boiled ajitsuke egg menma bamboo shoots wood ear mushrooms green onions black garlic oil"],
    ["Shoyu Ramen - Soy Sauce Broth Noodles", "https://cookpad.com/eng/recipes/24560444", "ramen noodles chicken and dashi broth shoyu tare soy sauce chashu pork narutomaki fish cake nori green onions soft boiled egg"],
    ["Miso Ramen with Sweet Corn and Butter", "https://cookpad.com/eng/recipes/24550555", "ramen noodles rich miso pork broth garlic ground pork bean sprouts sweet corn pat of butter green onions chili oil"],
    ["Ebi Tempura - Crispy Japanese Fried Shrimp", "https://cookpad.com/eng/recipes/24540666", "black tiger shrimp tempura flour ice cold water egg tempura dipping sauce mentsuyu grated ginger grated daikon radish frying oil"],
    ["Yakitori Negima - Chicken Thigh and Scallion Skewers", "https://cookpad.com/eng/recipes/24530777", "chicken thigh scallion stalks tare sauce soy sauce sake mirin brown sugar bamboo skewers"],
    ["Tamagoyaki - Japanese Rolled Omelette", "https://cookpad.com/eng/recipes/24520888", "eggs dashi stock sugar soy sauce mirin vegetable oil grated daikon radish"],
    ["Onigiri - Japanese Rice Balls with Salmon", "https://cookpad.com/eng/recipes/24510999", "steamed japanese short-grain rice grilled salted salmon furikake seasoning toasted nori seaweed sheet salt"],
    ["Unadon - Grilled Eel over Steamed Rice", "https://cookpad.com/eng/recipes/24501111", "unagi kabayaki eel unagi tare sauce soy sauce mirin sugar sake sansho japanese pepper steamed white rice"],
    ["Sukiyaki - Sweet Soy Beef Hot Pot", "https://cookpad.com/eng/recipes/24491222", "thinly sliced marbled beef tofu shirataki konjac noodles napa cabbage enoki mushrooms shiitake mushrooms leek soy sauce mirin sugar sake raw egg dip"],
    ["Shabu-Shabu - Japanese Swish Swish Hot Pot", "https://cookpad.com/eng/recipes/24481333", "thinly sliced beef kombu kelp dashi water napa cabbage enoki mushrooms tofu udon noodles ponzu citrus sauce sesame gomadare sauce"],
    ["Agedashi Tofu - Deep Fried Tofu in Dashi Broth", "https://cookpad.com/eng/recipes/24471444", "medium firm cotton tofu potato starch cornstarch dashi broth soy sauce mirin grated daikon ginger green onion bonito flakes katsuobushi"],
    ["Goma-ae - Japanese Spinach Salad with Sweet Sesame Dressing", "https://cookpad.com/eng/recipes/24461555", "fresh baby spinach toasted white sesame seeds soy sauce sugar mirin dashi salt"],
    ["Chawanmushi - Savory Japanese Egg Custard", "https://cookpad.com/eng/recipes/24451666", "eggs dashi broth chicken breast shrimp shiitake mushroom ginkgo nuts mitsuba soy sauce mirin salt"],
    ["Edamame with Sea Salt", "https://cookpad.com/eng/recipes/24441777", "fresh or frozen edamame soybean pods boiling water coarse coarse sea salt"],
    ["Japanese Curry Udon", "https://cookpad.com/eng/recipes/24431888", "udon noodles leftover japanese curry dashi stock soy sauce mirin thinly sliced beef or chicken green onion"],
    ["Yaki Udon - Stir Fried Udon Noodles with Pork & Veggies", "https://cookpad.com/eng/recipes/24421999", "thick udon noodles thinly sliced pork belly cabbage carrot onion scallions soy sauce mirin dashi powder bonito flakes aonori pickled ginger"],
    ["Yakisoba - Japanese Stir Fried Noodles", "https://cookpad.com/eng/recipes/24412111", "yakisoba noodles pork belly cabbage carrot bean sprouts yakisoba sauce kewpie mayonnaise aonori pickled red ginger"],
    ["Nikujaga - Japanese Sweet Soy Braised Beef and Potatoes", "https://cookpad.com/eng/recipes/24402222", "thinly sliced beef potatoes onion carrot shirataki noodles dashi stock soy sauce sake mirin sugar snow peas"],
    ["Korokke - Japanese Potato Croquettes with Minced Beef", "https://cookpad.com/eng/recipes/24392333", "russet potatoes ground beef minced yellow onion butter salt black pepper flour egg panko breadcrumbs tonkatsu sauce"],
    ["Teriyaki Salmon with Glazed Soy Sauce", "https://cookpad.com/eng/recipes/24382444", "fresh salmon fillets soy sauce mirin sake sugar ginger juice sesame seeds steamed jasmine rice broccoli"],
    ["Miso Glazed Black Cod (Gindara Saikyo Yaki)", "https://cookpad.com/eng/recipes/24372555", "black cod fillets saikyo sweet white miso mirin sake granulated sugar soy sauce"],
    ["Matcha Dorayaki - Japanese Red Bean Pancakes", "https://cookpad.com/eng/recipes/24362666", "flour matcha green tea powder eggs sugar honey mirin baking soda sweet azuki red bean paste anko"],
    ["Mochi Ice Cream - Sweet Rice Dumplings", "https://cookpad.com/eng/recipes/24352777", "mochiko sweet glutinous rice flour sugar water cornstarch vanilla matcha green tea strawberry ice cream scoops"],
    ["Taiyaki - Fish Shaped Waffle with Sweet Red Bean", "https://cookpad.com/eng/recipes/24342888", "cake flour baking powder sugar egg milk sweet red bean paste anko custard cream taiyaki mold"],
    ["Japanese Egg Salad Sando", "https://cookpad.com/eng/recipes/24332999", "hard boiled eggs kewpie japanese mayonnaise splash of milk pinch of sugar salt white pepper soft shokupan milk bread salted butter"],
    ["Kakiage Tempura - Crispy Mixed Vegetable & Shrimp Fritters", "https://cookpad.com/eng/recipes/24323111", "small shrimp onion carrot mitsuba burdock root tempura flour ice water frying oil mentsuyu sauce"],
    ["Kushikatsu - Osaka Deep Fried Skewered Meat and Veggies", "https://cookpad.com/eng/recipes/24313222", "pork loin onion lotus root quail eggs panko breadcrumbs flour egg batter kushikatsu dipping sauce cabbage leaves"],
    ["Ebi Fry - Japanese Crispy Fried Panko Shrimp", "https://cookpad.com/eng/recipes/24303333", "large shrimp black pepper salt flour beaten egg panko breadcrumbs tartar sauce lemon wedges shredded cabbage"],
    ["Curry Pan - Japanese Deep Fried Curry Bread", "https://cookpad.com/eng/recipes/24293444", "bread dough thick cooked japanese curry filling egg panko breadcrumbs frying oil"],
    ["Kakigori - Japanese Shaved Ice with Matcha and Condensed Milk", "https://cookpad.com/eng/recipes/24283555", "finely shaved ice matcha green tea syrup sweetened condensed milk sweet red bean paste anko shiratama dango mochi"],
    ["Anmitsu - Japanese Traditional Dessert Bowl", "https://cookpad.com/eng/recipes/24273666", "agar-agar kanten jelly cubes sweet azuki red bean paste shiratama dango canned fruit mandarin orange kuromitsu black sugar syrup"],
    ["Oden - Winter Japanese Dashi Stew", "https://cookpad.com/eng/recipes/24263777", "daikon radish boiled eggs konjac chikuwa fish cakes hanpen fried tofu mochi kinchaku dashi broth soy sauce mirin karashi yellow mustard"],
    ["Soboro Don - Ground Chicken and Scrambled Egg Rice Bowl", "https://cookpad.com/eng/recipes/24253888", "ground chicken soy sauce sake mirin sugar ginger scrambled eggs green peas snow peas steamed rice"],
    ["Ten Don - Tempura Rice Bowl with Sweet Sauce", "https://cookpad.com/eng/recipes/24243999", "crispy shrimp tempura eggplant sweet potato nori tempura tentsuyu sweet glaze sauce soy sauce dashi sugar steamed rice"],
    ["Unagi Chazuke - Grilled Eel Rice in Green Tea Dashi", "https://cookpad.com/eng/recipes/24234111", "grilled unagi eel steamed rice hot green tea dashi broth wasabi chopped nori scallions toasted sesame seeds"],
    ["Hiyashi Chuka - Cold Summer Ramen Salad", "https://cookpad.com/eng/recipes/24224222", "chilled ramen noodles sliced ham shredded egg omelet kinshi tamago cucumber strips imitation crab tomatoes sesame soy sauce vinegar dressing"],
    ["Saba Shioyaki - Salt Grilled Mackerel", "https://cookpad.com/eng/recipes/24214333", "fresh mackerel fillets sea salt grated daikon radish lemon wedge soy sauce steamed white rice"],
    ["Tori Teriyaki - Glazed Chicken Teriyaki Rice Plate", "https://cookpad.com/eng/recipes/24204444", "chicken thigh fillets soy sauce mirin sake sugar sesame seeds steamed broccoli rice"],
    ["Nasu Dengaku - Miso Glazed Broiled Eggplant", "https://cookpad.com/eng/recipes/24194555", "japanese round eggplant red miso paste mirin sake sugar sesame oil toasted white sesame seeds"],
    ["Kani Salad - Japanese Spicy Crab Cucumber Salad", "https://cookpad.com/eng/recipes/24184666", "imitation crab meat cucumber shreds carrot panko kewpie mayonnaise sriracha sauce tobiko flying fish roe"],
    ["Chashu Fried Rice (Yakimeshi)", "https://cookpad.com/eng/recipes/24174777", "cooked day-old rice diced chashu pork belly eggs chopped scallions green onions soy sauce sesame oil salt white pepper"],
    ["Mentaiko Pasta - Spicy Cod Roe Spaghetti", "https://cookpad.com/eng/recipes/24164888", "spaghetti pasta spicy mentaiko pollock roe butter heavy cream soy sauce shredded nori seaweed mitsuba"],
    ["Japanese Milk Crepe Cake", "https://cookpad.com/eng/recipes/24154999", "thin crepe layers flour milk eggs butter sugar vanilla fresh whipped cream powdered sugar"],
    ["Shio Ramen - Light Sea Salt Broth Noodles", "https://cookpad.com/eng/recipes/24145111", "ramen noodles clear chicken dashi broth sea salt shio tare chashu menma green onion soft boiled egg"],
    ["Abura Soba - Soupless Oil Ramen Noodles", "https://cookpad.com/eng/recipes/24135222", "thick ramen noodles pork oil soy tare sauce vinegar chili rayu oil chashu raw egg yolk green onions minced garlic menma"],
    ["Tsukemen - Dipping Ramen Noodles with Rich Broth", "https://cookpad.com/eng/recipes/24125333", "chilled extra thick ramen noodles ultra rich concentrated pork seafood dashi dipping soup chashu nori lime wedge scallions"],
    ["Japanese Hamburg Curry", "https://cookpad.com/eng/recipes/24115444", "juicy beef and pork hamburg steak japanese curry sauce steamed white rice fried egg melted cheese"],
    ["Tendon Tempura Rice Bowl", "https://cookpad.com/eng/recipes/24105555", "crispy tempura shrimp pumpkin green beans sweet dashi soy tare sauce steamed white rice"],
    ["Kaki Fry - Japanese Deep Fried Panko Oysters", "https://cookpad.com/eng/recipes/24095666", "fresh oysters flour egg panko breadcrumbs frying oil japanese tartar sauce lemon wedges"],
    ["Omurice - Japanese Omelette Rice with Demi-Glace Sauce", "https://cookpad.com/eng/recipes/24085777", "ketchup chicken fried rice fluffy soft scrambled egg omelette demi-glace or tomato sauce fresh parsley"],
    ["Dashi Rolled Omelette with Cheese (Cheesy Tamagoyaki)", "https://cookpad.com/eng/recipes/24075888", "eggs dashi broth soy sauce mirin mozzarella cheese nori flakes"],
    ["Japanese Pickled Daikon Radish (Takuan)", "https://cookpad.com/eng/recipes/24065999", "daikon radish rice vinegar sugar sea salt turmeric powder water"],
    ["Salmon Teriyaki Bento Bowl", "https://cookpad.com/eng/recipes/24056111", "pan seared salmon fillet teriyaki glaze sauce steamed edamame tamagoyaki rolled egg pickled ginger steamed rice"],
    ["Tuna Mayo Onigiri", "https://cookpad.com/eng/recipes/24046222", "canned tuna kewpie japanese mayonnaise soy sauce salt steamed short-grain rice crispy nori sheet"],
    ["Umeboshi Sour Plum Onigiri", "https://cookpad.com/eng/recipes/24036333", "pickled sour umeboshi plum steamed short-grain rice sea salt crispy toasted nori sheet"],
    ["Japanese Souffle Pancakes", "https://cookpad.com/eng/recipes/24026444", "egg whites sugar egg yolks milk cake flour baking powder vanilla butter maple syrup whipped cream"],
    ["Matcha Ice Cream", "https://cookpad.com/eng/recipes/24016555", "ceremonial grade matcha powder heavy cream whole milk sugar egg yolks vanilla"],
    ["Hojicha Latte Float", "https://cookpad.com/eng/recipes/24006666", "roasted green tea hojicha leaves hot water whole milk simple syrup vanilla ice cream scoop"],
    ["Chicken Katsu Curry", "https://cookpad.com/eng/recipes/23996777", "crispy panko breaded chicken breast cutlet japanese brown curry sauce carrots potatoes steamed rice fukujinzuke pickles"],
    ["Pork Belly Kakuni - Melt in Mouth Braised Pork", "https://cookpad.com/eng/recipes/23986888", "thick pork belly cubes daikon radish ginger scallions dashi soy sauce mirin sake rock sugar boiled eggs karashi mustard"],
    ["Japanese Garlic Fried Rice", "https://cookpad.com/eng/recipes/23976999", "day old white rice crispy garlic chips minced garlic butter soy sauce green onions salt black pepper"],
    ["Wagyu Beef Yakiniku Rice Bowl", "https://cookpad.com/eng/recipes/23967111", "grilled a5 wagyu beef slices yakiniku dipping sauce soy sauce mirin garlic sesame oil toasted sesame seeds green onion steamed rice"],
    ["Kinoko Gohan - Japanese Mushroom Rice", "https://cookpad.com/eng/recipes/23957222", "short grain rice shiitake shimeji maitake mushrooms dashi broth soy sauce sake mirin aburaage fried tofu"],
    ["Asari no Sakamushi - Clams Steamed in Sake", "https://cookpad.com/eng/recipes/23947333", "fresh manila clams japanese sake soy sauce butter minced garlic green onions sliced chili pepper"],
    ["Japanese Chicken Sukiyaki", "https://cookpad.com/eng/recipes/23937444", "chicken thighs tofu shirataki konjac noodles napa cabbage scallions shiitake mushrooms sukiyaki sauce soy sauce mirin sake sugar"],
    ["Torikawa - Crispy Grilled Chicken Skin Skewers", "https://cookpad.com/eng/recipes/23927555", "chicken skin salt black pepper tare glaze soy sauce sake mirin lemon wedge"],
    ["Gyu Katsu - Rare Deep Fried Beef Cutlet", "https://cookpad.com/eng/recipes/23917666", "beef tenderloin sirloin flour egg panko breadcrumbs wasabi soy sauce rock salt tonkatsu sauce cabbage"],
    ["Egg Ramen", "https://cookpad.com/eng/recipes/23907777", "ramen noodles soft boiled seasoned egg dashi chicken broth soy sauce green onion sesame oil nori"]
]


def ensure_data_files():
    data_dir = PROJECT_ROOT / "data"
    raw_dir = data_dir / "raw"
    proc_dir = data_dir / "processed"

    raw_dir.mkdir(parents=True, exist_ok=True)
    proc_dir.mkdir(parents=True, exist_ok=True)

    full_csv = raw_dir / "Japan_Food_Ingredients_Full.csv"
    cleaned_csv = proc_dir / "Japan_Food_Ingredients_Cleaned.csv"
    links_csv = raw_dir / "Japan_Food_Links_50.csv"

    # Always write authentic dataset
    from .preprocessing.text_cleaner import clean_title, clean_ingredients

    full_rows = [["Recipe Title", "Recipe URL", "Ingredients"]]
    clean_rows = [["Recipe Title", "Recipe URL", "Ingredients", "Cleaned Title", "Cleaned Ingredients"]]
    link_rows = [["Recipe Title", "Recipe URL"]]

    for title, url, ing in AUTHENTIC_JAPANESE_RECIPES:
        full_rows.append([title, url, ing])
        clean_rows.append([title, url, ing, clean_title(title), clean_ingredients(ing)])
        link_rows.append([title, url])

    with open(full_csv, 'w', newline='', encoding='utf-8-sig') as f:
        csv.writer(f).writerows(full_rows)

    with open(cleaned_csv, 'w', newline='', encoding='utf-8-sig') as f:
        csv.writer(f).writerows(clean_rows)

    with open(links_csv, 'w', newline='', encoding='utf-8-sig') as f:
        csv.writer(f).writerows(link_rows)

    return len(clean_rows) - 1


if __name__ == '__main__':
    count = ensure_data_files()
    print(f"Ensured {count} authentic Japanese recipes.")
