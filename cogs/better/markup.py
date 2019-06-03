markup=lambda string, sufix='```': sufix + string + sufix
markdown=lambda string, lang='markdown': markup(lang+'\n'+string)

bitalic=lambda string: markup(string, '***')
italic=lambda string: markup(string, '*')
bold=lambda string: markup(string, '**')

