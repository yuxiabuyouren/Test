from rdflib import Graph
import pprint
import queue

def getData(path, disease_name):
    links = []
    treatments = []
    drugs = []

    g = Graph()
    g.parse(path, format="nt")

    nodes = [{'category': 'disease',
             'name': disease_name,
             'x': '100',
             'y': '50',
             'fixed': 'true',
             'draggable': 'true'
            }]

    # 查询第一个治疗id及名称
    qrel = g.query(
        """
        PREFIX : <http://www.mydemo.com#>
        SELECT ?s ?o
        WHERE {  
            ?d :disease_name "oesophageal and gastric cancer" .
            ?d :treatedby ?s .
            ?s :treatment_name ?o .
        }
        """
    )

    for row in qrel:
        first = row[0].split('/')[-1]

    q = queue.Queue()
    q.put(first)

    # 查询所有的治疗步骤
    while not q.empty():
        id = q.get()
        
        # 查询所有治疗步骤
        qrel = g.query(
            """
            PREFIX : <http://www.mydemo.com#>
            SELECT ?next_id ?pre_name ?next_name ?condition
            WHERE {  
                ?s :treatment_id %s.
                ?s :nextstep ?next_id .
                ?s :treatment_name ?pre_name .
                ?next_id :treatment_name ?next_name .
                optional{?next_id :treatment_conditions ?condition}
            }
            """ % (id)
        )

        for row in qrel:
            q.put(row[0].split('/')[-1])
            link = {'source': str(row[1]), 'target': str(row[2]), 'value': str(row[3])}
            links.append(link)

        # 查询结点的属性
        qrel = g.query(
            """
            PREFIX : <http://www.mydemo.com#>
            SELECT ?name ?type ?description
            WHERE {
                ?s :treatment_id %s .
                ?s :treatment_name ?name .
                ?s :treatment_description ?description .
                optional{?s :treatment_type ?type}
            }
            """ % (id)
        )
        
        for row in qrel:
            treatment = {
             'category': 'treatment',
             'name': str(row[0]),
             'draggable': 'true',
             'value': {'type': str(row[1]), 'description': str(row[2])}
            }
            name = str(row[0])
            treatments.append(treatment)
        
        # 查询节点用药
        qrel = g.query(
            """
            PREFIX : <http://www.mydemo.com#>
            SELECT ?name ?time ?period ?dosage
            WHERE {
                ?s :treatment_id %s.
                ?s :use ?drug_id.
                ?drug_id :drug_name ?name.
                optional{?drug_id :drug_time ?time}
                optional{?drug_id :drug_dosage ?dosage}
                optional{?drug_id :drug_period ?period}
            }
            """ % (id)
        )

        for row in qrel:
            link = {'source': name, 'target': str(row[2]), 'value': str(row[3])}
            links.append(link)

            drug = {'category': 'drug',
                'name': str(row[0]),
                'draggable': 'true',
                'value': {'time' : str(row[1]), 'period': str(row[2]), 'dosage':str(row[3])}}
            drugs.append(drug)

    nodes.extend(treatments)
    nodes.extend(drugs)  
    return links, nodes 

if __name__ == "__main__":
    path = "myDemo.nt"
    disease_name = "oesophageal and gastric cancer"
    getData(path, disease_name)