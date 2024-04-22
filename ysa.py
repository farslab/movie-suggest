import pandas as pd
import numpy as np
import argparse
import json
pd.set_option('display.max_rows', None)  # Tüm satırları göstermek için None olarak ayarla
pd.set_option('display.max_columns', None)  # Tüm sütunları göstermek için
pd.set_option('display.width', None)        # Genişliği arttırarak okunabilirliği arttırır

# Veri setlerini yükle
movies = pd.read_csv('dataset1mb/movies.csv')
ratings = pd.read_csv('dataset1mb/ratings.csv')
# Filmler ve puanlar verilerini birleştir
merged_data=pd.read_csv('merged_data.csv')
# Create a parser object
parser = argparse.ArgumentParser(description="A script for recommending movies based on user ID")
# Add user_id argument to the parser
parser.add_argument("user_id", type=int, help="User ID for which to recommend movies")
# Parse the arguments
args = parser.parse_args()
# Use the user_id in the code
user_id = args.user_id
# Now, you can use 'user_id' wherever you need it in your code
# Kullanıcı-film matrisini oluştur
user_movie_matrix = merged_data.pivot_table(index='userId', columns='title', values='rating')
# İzlenen filmleri ve puanları görüntüleme
class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        # Ağırlıkları ve biasları başlat
        self.weights1 = np.random.randn(input_size, hidden_size) * 0.01
        self.weights2 = np.random.randn(hidden_size, output_size) * 0.01
        self.bias1 = np.zeros((1, hidden_size))
        self.bias2 = np.zeros((1, output_size))

    def sigmoid(self, x):
        # Sigmoid aktivasyon fonksiyonu
        x = np.clip(x, -500, 500)  # x değerlerini -500 ile 500 arasında sınırla
        return 1 / (1 + np.exp(-x))

    def sigmoid_derivative(self, x):
        # Sigmoid'in türevi
        return x * (1 - x)

    def forward(self, x):
        # İleri besleme işlemi
        self.hidden = self.sigmoid(np.dot(x, self.weights1) + self.bias1)
        self.output = self.sigmoid(np.dot(self.hidden, self.weights2) + self.bias2)
        return self.output

    def backprop(self, x, y, o):
        # Geri yayılım işlemi
        self.error = y - o
        self.d_output = self.error * self.sigmoid_derivative(o)
        self.error_hidden = self.d_output.dot(self.weights2.T)
        self.d_hidden = self.error_hidden * self.sigmoid_derivative(self.hidden)

        # Ağırlık ve bias güncellemeleri
        self.weights1 += x.T.dot(self.d_hidden)
        self.weights2 += self.hidden.T.dot(self.d_output)
        self.bias1 += np.sum(self.d_hidden, axis=0, keepdims=True)
        self.bias2 += np.sum(self.d_output, axis=0, keepdims=True)

    def train(self, X, Y, epochs=100):
        for epoch in range(epochs):
            # İleri besleme
            o = self.forward(X)

            # Geri yayılım
            self.backprop(X, Y, o)

    def predict(self, x):
        # Tahmin işlemi için ileri besleme
        hidden = self.sigmoid(np.dot(x, self.weights1) + self.bias1)
        output = self.sigmoid(np.dot(hidden, self.weights2) + self.bias2)
        return output

def select_top_n(predictions, movie_titles, n=5):
    # predictions dizisinin boyutunu düzelt
    predictions = predictions.flatten()  # Tahminleri tek bir boyuta düzelt
    # Tahminlerden en yüksek puan alan 'n' filmin indekslerini al
    top_n_indices = predictions.argsort()[-n:][::-1]
    # Bu indekslere karşılık gelen film isimlerini al
    top_n_movies = movie_titles[top_n_indices]
    return list(top_n_movies)

# Verileri ve model parametrelerini belirle
input_size = user_movie_matrix.shape[1]
hidden_size = 10  # Bu parametre deneylerle belirlenmelidir
output_size = user_movie_matrix.shape[1]  # Kullanıcı tarafından verilen tüm filmler için puanlar

# Kullanıcı-film matrisini numpy array'ine dönüştür (NaN değerleri 0 ile değiştir)
X_train = np.nan_to_num(user_movie_matrix.to_numpy())

# YSA modelini başlat ve eğit
nn = NeuralNetwork(input_size, hidden_size, output_size)
nn.train(X_train, X_train, epochs=100)  # Burada X_train'i hem giriş hem de çıktı olarak kullanıyoruz çünkü bir tür otoencoder yapıyoruz.


# Bu kullanıcı için tüm filmlere tahminler yap
user_profile = X_train[user_id - 1]  # Kullanıcı ID'sine göre profil seçimi

predictions = nn.predict(user_profile)
print("Tahminler:", predictions)

# Film başlıklarını al
movie_titles = np.array(user_movie_matrix.columns)

# En yüksek puan alan filmleri seç
recommended_movies = select_top_n(predictions.flatten(), movie_titles, n=5)  # predictions'ı tek boyuta indirge
recommended_movies_dict = {}
if len(recommended_movies) > 0:
    recommended_details = movies[movies['title'].isin(recommended_movies)]
    recommended_movies_dict = recommended_details[['title', 'genres']].to_dict(orient='records')


def display_average_ratings(recommended_movies, merged_data):
    print("Önerilen Filmlerin Ortalama Puanları:")
    for title in recommended_movies:
        average_rating = merged_data[merged_data['title'] == title]['rating'].mean()
        print(f"{title}: {average_rating:.3f}")



# Seçilen indeksleri yazdır
top_n_indices = predictions.argsort()[-5:][::-1]  # Burada 5, seçmek istenilen film sayısıdır.
print("Seçilen indeksler:", top_n_indices)

# Önerilen filmlerin ortalama puanlarını göster
display_average_ratings(recommended_movies, merged_data)

def get_recommendations(recommended_movies_dict):
    recommendations_json = json.dumps(recommended_movies_dict)
    return {'recommendations': recommendations_json}

# JSON cevabını döndür
get_recommendations(recommended_movies_dict)