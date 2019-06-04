limit=lambda string, max=32: string[:max] + ('', '...')[len(list(string)) > max]
