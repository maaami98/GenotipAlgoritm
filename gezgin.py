
import random
import operator
from numpy import vectorize
class geneticAlgoriması():
    
    def __init__(self,hash_map,başlangıç,steps=2,caprazlama_oran=0.15,mutasuon_oranı=0.15,population_size=5,iterasyon=100):
        self.caprazlama_oran=caprazlama_oran
        self.mutasuon_oranı=mutasuon_oranı
        self.population_size=population_size
        self.hash_map = hash_map
        self.steps = steps
        self.iterasyon = iterasyon
        self.başlangıç = başlangıç
        self.nokta = [k for k in self.hash_map.keys()] 
        self.nokta.remove(başlangıç)
        self.nesiller = []
        self.epsilon = 1 - 1/self.iterasyon        
        self.nesil_uret = vectorize(self.nesil_uret)
        self.kararlılık = vectorize(self.kararlılık)
        self.mutatlaşma = vectorize(self.mutatlaşma)
        self.prune_nesiller = vectorize(self.prune_nesiller)
        self.converge = vectorize(self.converge)

        
        self.nesil_uret()
        
    def nesil_uret(self):
        for i in range(self.population_size):
            nesil = [self.başlangıç]
            options = [k for k in self.nokta]
            while len(nesil) < len(self.nokta)+1:
                n = random.choice(options)
                loc = options.index(n)
                nesil.append(n)
                del options[loc]
            nesil.append(self.başlangıç)
            self.nesiller.append(nesil)
        return self.nesiller
    
    def kararlılık(self):
        kararlılık_puanı = []
        for nesil in self.nesiller:
            toplam_uzaklık = 0
            for idx in range(1,len(nesil)):
                b_noktası = nesil[idx]
                a_noktası = nesil[idx-1]
                try:
                    uzak = self.hash_map[a_noktası][b_noktası]
                except:
                    uzak = self.hash_map[b_noktası][a_noktası]
                toplam_uzaklık += uzak
            kısalık = 1/toplam_uzaklık
            kararlılık_puanı.append(kısalık)
        return kararlılık_puanı
    
    def mutatlaşma(self):
        index_map = {i:'' for i in range(1,len(self.nokta)-1)}
        indices = [i for i in range(1,len(self.nokta)-1)]
        to_visit = [c for c in self.nokta]
        capraz = (1 - self.epsilon) * self.caprazlama_oran
        mutate = self.epsilon * self.mutasuon_oranı 
        caprazlanan_n = int(capraz * len(self.nokta)-1)
        mutant = int((mutate * len(self.nokta)-1)/2)
        for idx in range(len(self.nesiller)-1):
            nesil = self.nesiller[idx]
            for i in range(caprazlanan_n):
                try:
                    nesil_index = random.choice(indices)
                    sample = nesil[nesil_index]
                    if sample in to_visit:
                        index_map[nesil_index] = sample
                        loc = indices.index(nesil_index)
                        del indices[loc]
                        loc = to_visit.index(sample)
                        del to_visit[loc]
                    else:
                        continue
                except:
                    pass
        last_nesil = self.nesiller[-1]
        remaining_nokta = [c for c in last_nesil if c in to_visit]
        for k,v in index_map.items():
            if v != '':
                continue
            else:
                city = remaining_nokta.pop(0)
                index_map[k] = city
        new_nesil = [index_map[i] for i in range(1,len(self.nokta)-1)]
        new_nesil.insert(0,self.başlangıç)
        new_nesil.append(self.başlangıç)
        for i in range(mutant):
            seçim = [c for c in new_nesil if c != self.başlangıç]
            a_noktası = random.choice(seçim)
            b_noktası = random.choice(seçim)
            index_a = new_nesil.index(a_noktası)
            index_b = new_nesil.index(b_noktası)
            new_nesil[index_a] = b_noktası
            new_nesil[index_b] = a_noktası
        self.nesiller.append(new_nesil)
                
    def prune_nesiller(self):       
        for i in range(self.steps):
            self.mutatlaşma()
        kararlılık_puanı = self.kararlılık()
        for i in range(self.steps):
            kötü_nesil_id = kararlılık_puanı.index(min(kararlılık_puanı))
            del self.nesiller[kötü_nesil_id]
            del kararlılık_puanı[kötü_nesil_id]
        return max(kararlılık_puanı),self.nesiller[kararlılık_puanı.index(max(kararlılık_puanı))]
    
    def converge(self):
        for i in range(self.iterasyon):
            değerler = self.prune_nesiller()
            current_score = değerler[0]
            şimdiki_eniyi_nesil = değerler[1]
            self.epsilon -= 1/self.iterasyon
            if i % 100 == 0:
                print(f"{int(1/current_score)} birim")
                
        return şimdiki_eniyi_nesil


nokta = """
A
B
C
D
"""
nokta=[c for c in nokta.split('\n') if c != '']
nokta_uzaklık={c:{} for c in nokta}
nokta_uzaklık["A"]["B"] = 7
nokta_uzaklık["A"]["C"] = 9
nokta_uzaklık["A"]["D"] = 8
nokta_uzaklık["B"]["C"] = 11
nokta_uzaklık["B"]["D"] = 7
nokta_uzaklık["C"]["D"] = 4

g = geneticAlgoriması(hash_map=nokta_uzaklık,başlangıç="A",mutasuon_oranı=0.25,caprazlama_oran=0.5,
                 population_size=150,steps=15,iterasyon=2000)
g.converge()