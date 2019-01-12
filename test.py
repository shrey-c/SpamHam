import pickle


loaded_model = pickle.load(open('finalized_model.sav', 'rb'))
print(loaded_model)
