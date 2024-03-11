from queue import PriorityQueue


# informatii despre un nod din arborele de parcurgere (nu nod din graful initial)
class Nod:
    def __init__(self, info, parinte=None, g=0, h=0):
        self.info = info  # eticheta nodului
        self.parinte = parinte  # parintele din arborele de parcurgere
        self.g = g  # costul drumului de la radacina pana la nodul curent
        self.h = h  # costul estimat de la nodul curent pana la nodul scop
        self.f = self.g + self.h  # costul total (f = g + h)

    def __str__(self):
        return str(self.info)

    def __repr__(self):
        # afisarea unui nod va fi de forma "c (a -> b -> c)"
        return "({}, ({}))".format(self.info, "->".join([str(x) for x in self.drumRadacina()]))

    def __eq__(self, other):
        return self.f == other.f and self.g==other.g

    def __le__(self, other):
        return self < other or self == other

    def __lt__(self, other):
        return self.f < other.f or (self.f == other.f and self.g > other.g)

    # va returna o listă cu toate nodurile ca obiecte de la rădăcină până la nodul curent
    def drumRadacina(self):
        l = []
        while self is not None:
            l.insert(0, self)
            self = self.parinte  # trec la parintele din arborele de parcurgere
        return l

    # verifică dacă nodul a fost vizitat (informatia lui e in propriul istoric)
    def vizitat(self):
        nod = self.parinte
        while nod is not None:
            if self.info == nod.info:
                return True
            nod = nod.parinte
        return False


class Graf:  # graful problemei

    def __init__(self, mat, start, scopuri, h):
        self.mat = mat  # matricea de adiacenta
        self.start = start  # informatia nodului de start
        self.scopuri = scopuri  # lista cu informatiile nodurilor scop
        self.h = h  # euristica

    # verifica daca nodul curent este un nod scop
    def scop(self, infoNod):
        return infoNod in self.scopuri

    def estimeaza_h(self, info):
        return self.h[info]

    # va genera succesorii sub forma de noduri in arborele de parcurgere
    def succesori(self, nodCurent):
        Succ = []
        for i in range(len(self.mat)):
            if self.mat[nodCurent.info][i] > 0:
                nodNou = Nod(i, nodCurent, nodCurent.g +
                             self.mat[nodCurent.info][i], self.estimeaza_h(i))
                if not nodNou.vizitat():
                    Succ.append(nodNou)
        return Succ

######################################################################### A* cu mai multe solutii ###################################


def binarySearch(lNoduri, nodNou, ls, ld):
    if len(lNoduri) == 0:
        return 0
    if ls == ld:
        if nodNou.f < lNoduri[ls].f:
            return ls
        elif nodNou.f > lNoduri[ls].f:
            return ld+1
        else:
            if nodNou.g < lNoduri[ls].g:
                return ld+1
            else:
                return ls
    else:
        m = (ls+ld)//2
        if nodNou.f < lNoduri[m].f:
            return binarySearch(lNoduri, nodNou, ls, m)
        elif nodNou.f > lNoduri[m].f:
            return binarySearch(lNoduri, nodNou, m+1, ld)
        else:
            if nodNou.g > lNoduri[m].g:
                return binarySearch(lNoduri, nodNou, ls, m)
            else:
                return binarySearch(lNoduri, nodNou, m+1, ld)


def aStarSM(gr, nrSol=1):
    # in coada avem noduri (obiecte de tip Nod)
    q = [Nod(gr.start)]

    while len(q) > 0:
        nodCurent = q.pop(0)  # sterg primul element din coada
        # trebuie pus in close nodul curent
        # nu trebuie sa am in open si close aceeasi informatie de 2 ori
        # pentru fiecare succesor trebuie sa verific daca nu cumva exista in close/open
        # daca are succesorul mai mare, atunci ignor, altfel sterg nodul vechi din open si close si adaug pe cel nou
        if gr.scop(nodCurent.info):  # daca nodul curent este scop
            print("SOL: ", end="")  # afisez solutia
            print(repr(nodCurent))
            print("Drum de cost: ", nodCurent.g)
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            nrSol -= 1  # am gasit o solutie, deci scad nr de solutii
            if nrSol == 0:
                return
        # generez succesorii nodului curent
        lSuccesori = gr.succesori(nodCurent)
        # q += lSuccesori
        for s in lSuccesori:
            i = binarySearch(q, s, 0, len(q)-1)
            if i == len(q):
                q.append(s)
            else:
                q.insert(i, s)

######################################################################### A* cu mai multe solutii si PQ #############################


def aStarSM_PQ(gr, nrSol=1):
    # in coada avem noduri (obiecte de tip Nod)
    q = PriorityQueue(0)
    q.put(Nod(gr.start))
    while q.qsize() > 0:
        nodCurent = q.get()  # sterg primul element din coada
        if gr.scop(nodCurent.info):  # daca nodul curent este scop
            print("SOL: ", end="")  # afisez solutia
            print(repr(nodCurent))
            print("Drum de cost: ", nodCurent.g)
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            nrSol -= 1  # am gasit o solutie, deci scad nr de solutii
            if nrSol == 0:
                return
        # generez succesorii nodului curent
        lSuccesori = gr.succesori(nodCurent)
        # q += lSuccesori
        for s in lSuccesori:
            q.put(s)

######################################################################### A* ########################################################


def in_list(nod_info, lista):
    for nod in lista:
        if nod_info == nod.info:
            return nod
    return None


def insert(node, lista):
    i = 0
    # cautam pozitia de inserare in lista
    # nodurile sunt sortate crescator dupa f
    # daca f-urile sunt egale, atunci crescator dupa g
    # astfel, sortam nodurile astfel incat sa fie cat mai apropiate de nodul scop
    while i < len(lista) - 1 and (node.f > lista[i].f or (node.f == lista[i].f and node.g < lista[i].g)):
        i += 1
    lista.insert(i, node)


def a_star(gr):
    opened = [Nod(gr.start)]  # nodurile neexpandate

    closed = []  # nodurile expandate
    continue_search = True  # daca am ajuns la scop sau nu

    # cat timp mai am noduri neexpandate si nu am ajuns la scop
    while len(opened) > 0 and continue_search:
        # se extrage primul nod, n, din lista open si se pune in closed
        nodCurent = opened.pop(0)
        closed.append(nodCurent)

        # daca nodul curent este nodul scop, oprim cautarea si afisam drumul de la nodul-start pana la nodul curent
        if gr.scop(nodCurent.info):
            print("SOL: ", end="")  # afisez solutia
            print(repr(nodCurent))
            print("Drum de cost: ", nodCurent.g)
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            continue_search = False  # am gasit o solutie, deci oprim cautarea

        # extindem nodul curent, obtinandu-i toti succesori
        # toti succesorii il au ca parinte pe n
        lSuccesori = gr.succesori(nodCurent)

        for s in lSuccesori:
            info, h, g = s.info, s.h, s.g
            nod_o = in_list(info, opened)  # nodul s este in lista opened
            nod_pargurgere = Nod(info, nodCurent, g, g+h)
            if nod_o:
                if nod_o.f > g+h:  # in cazul in care s-a gasit un succesor cu f mai bun, nodul vechi se sterge si se insereaza noul nod
                    opened.remove(nod_o)
                    insert(nod_pargurgere, opened)
                continue
            nod_c = in_list(info, closed)
            if nod_c:
                if nod_c.f > g+h:  # in cazul in care s-a gasit un succesor cu f mai bun, nodul vechi se sterge si se insereaza noul nod
                    closed.remove(nod_c)
                    insert(nod_pargurgere, opened)
                continue
            insert(nod_pargurgere, opened)

    if (len(opened) == 0):
        print("Nu exista solutie")


m = [
   # 0  1  2  3  4  5  6 
    [0, 3, 5, 10, 0, 0, 100],
    [0, 0, 0, 4, 0, 0, 0],
    [0, 0, 0, 4, 9, 3, 0],
    [0, 3, 0, 0, 2, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 4, 0, 5],
    [0, 0, 3, 0, 0, 0, 0]
]

start = 0
scopuri = [4, 6]
h = [0, 1, 6, 2, 0, 3, 0]
h_admisibile = [0, 2, 5, 4, 0, 3, 0]
# h_neadmisibile = [0, 1, 6, 12, 0, 3, 0]

gr = Graf(m, start, scopuri, h)


print("============================= \nA*multi\n")
aStarSM(gr, 2)
print("============================= \nA*multi cu PQ\n")
aStarSM_PQ(gr, 2)
print("============================= \nA*\n")
aStarSM_PQ(gr)

gr = Graf(m, start, scopuri, h_admisibile)


print("============================= \nA*multi\n")
aStarSM(gr, 2)
print("============================= \nA*multi cu PQ\n")
aStarSM_PQ(gr, 2)
print("============================= \nA*\n")
aStarSM_PQ(gr)