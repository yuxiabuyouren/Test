from rdflib import Graph
import queue

def getData(path, disease_name):
    links = []
    treatments = []
    drugs = []
    nodes = []

    try:
        g = Graph()
        g.parse(path, format="nt")

        # 查询第一个治疗id及名称
        qrel = g.query(
            """
            PREFIX : <http://www.mydemo.com#>
            SELECT ?s
            WHERE {  
                ?d :disease_name "%s" .
                ?d :treatedby ?s .
            }
            """ % (disease_name)
        )

        if qrel:
            nodes.append({'category': 'disease',
                'id': 0,
                'name': disease_name,
                'x': '100',
                'y': '50',
                'fixed': 'true',
                'draggable': 'true',
                'value': {'name': disease_name}
                })

            q = queue.Queue()
            saved = []
            saved_drug = []

            for row in qrel:
                first = row[0].split('/')[-1]
                link = {'source': 0, 'target': 't' + first, 'value': 'None'}
                links.append(link)
                if first not in saved:
                    saved.append(first)
                    q.put(first)

            # 查询所有的治疗步骤
            while not q.empty():
                id = q.get()
                
                # 查询所有治疗步骤
                qrel = g.query(
                    """
                    PREFIX : <http://www.mydemo.com#>
                    SELECT ?next_id ?condition
                    WHERE {  
                        ?s :treatment_id %s.
                        ?s :nextstep ?next_id .
                        optional{?next_id :treatment_conditions ?condition}
                    }
                    """ % (id)
                )

                for row in qrel:
                    nextId = row[0].split('/')[-1]
                    link = {'source': 't' + id, 'target': 't' + nextId, 'value': str(row[1])}
                    links.append(link)
                    if nextId not in saved:
                        saved.append(nextId)
                        q.put(nextId)

                # 查询结点的属性
                qrel = g.query(
                    """
                    PREFIX : <http://www.mydemo.com#>
                    SELECT ?name ?type ?description ?intention ?time
                    WHERE {
                        ?s :treatment_id %s .
                        ?s :treatment_name ?name .
                        ?s :treatment_description ?description .
                        optional{?s :treatment_type ?type}
                        optional{?s :treatment_intension ?intention}
                        optional{?s :treatment_time ?time}
                    }
                    """ % (id)
                )
                
                for row in qrel:
                    treatment = {
                    'category': 'treatment',
                    'id': 't' + id, 
                    'name': str(row[0]),
                    'draggable': 'true',
                    'value': {'name': str(row[0]), 
                              'type': str(row[1]), 
                              'time': str(row[4]),
                              'intention': str(row[3]),
                              'description': str(row[2])}
                    }
                    # name = str(row[0])
                    treatments.append(treatment)
                
                # 查询节点用药
                qrel = g.query(
                    """
                    PREFIX : <http://www.mydemo.com#>
                    SELECT ?name ?time ?period ?dosage ?drug_id
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
                    drug_id = row[4].split('/')[-1]
                    link = {'source': 't' + id, 'target': 'd' + drug_id, 'value': 'None'}
                    links.append(link)

                    if drug_id not in saved_drug:
                        drug = {'category': 'drug',
                            'id': 'd' + drug_id,
                            'name': str(row[0]),
                            'draggable': 'true',
                            'value': {'name': str(row[0]),'time' : str(row[1]), 'period': str(row[2]), 'dosage':str(row[3])}}
                        drugs.append(drug)
                        saved_drug.append(drug_id)

            nodes.extend(treatments)
            nodes.extend(drugs) 
            # print(sorted(saved))
            # print(sorted(saved_drug))
    except Exception as e:
        print(e)
    
    return links, nodes 

if __name__ == "__main__":
    path = "treat.nt"
    disease_name = "Blood_and_bone_marrow_cancers"
    links, nodes = getData(path, disease_name)
    # print(nodes)
    print(links)