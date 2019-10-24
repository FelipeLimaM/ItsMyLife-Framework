



class Routine():
    def __init__(self, df):
        self.df = df

    def build (self):
        # para cada linha
        for aux, row in self.df.iterrows():
