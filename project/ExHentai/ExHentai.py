from apis.ExHentaiApi import ExHentai, ExCat

hentai = ExHentai()
hentai.set_filter(ExCat.Doujinshi | ExCat.Manga)
hentai.list_works()
