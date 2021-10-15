import requests
from requests.auth import HTTPBasicAuth

users = [["pierre.bellegueule@gmx.fr", "123456789@", 4],["jean@yves.fr", "123456789@", 2],["jean@jean.fr", "123456789@", 3]]

# Test each endpoint with authorizations

# 2 is Support Team
# 3 is Sales Team
# 4 is Admin Team

def test_contacts_get():
    for user in users:
        username = user[0]
        password = user[1]
        authorization = user[2]

        res = requests.get(
            'http://127.0.0.1:8000/contracts/',
            auth=HTTPBasicAuth(username, password),
        )

        data = res.json()

        if authorization == 4:
            assert len(data) == 4
            ids = [3, 5, 6, 7]
            for contract in data:
                if not contract['id'] in ids:
                    assert False
            assert True

        if authorization == 3:
            assert len(data) == 2
            ids = [3, 5]
            for contract in data:
                if not contract['id'] in ids:
                    assert False
            assert True

        if authorization == 2:
            assert data['detail'] == "Vous n'avez pas la permission d'effectuer cette action."

def test_contract_update():
    for user in users:
        username = user[0]
        password = user[1]
        authorization = user[2]

        res = requests.put(
            'http://127.0.0.1:8000/contracts/3',
            auth=HTTPBasicAuth(username, password),
        )
        data = res.json()

        if authorization == 4:
            assert data['title'][0]

        if authorization == 3:
            assert data['title'][0]

        if authorization == 2:
            assert data['detail'] == "Vous n'avez pas la permission d'effectuer cette action."

def test_contract_post():
    for user in users:
        username = user[0]
        password = user[1]
        authorization = user[2]

        res = requests.post(
            'http://127.0.0.1:8000/contracts/',
            auth=HTTPBasicAuth(username, password),
        )
        data = res.json()
        if authorization == 4:
            assert data['title'][0] == 'Ce champ est obligatoire.'

        if authorization == 3:
            assert data['title'][0] == 'Ce champ est obligatoire.'

        if authorization == 2:
            assert data['detail'] == "Vous n'avez pas la permission d'effectuer cette action."

def test_customers_get():
    for user in users:
        username = user[0]
        password = user[1]
        authorization = user[2]

        res = requests.get(
            'http://127.0.0.1:8000/customers/',
            auth=HTTPBasicAuth(username, password),
        )
        data = res.json()

        if authorization == 4:
            assert len(data) == 2
            ids = [1,2]
            for customer in data:
                if not customer['id'] in ids:
                    assert False
            assert True

        if authorization == 3:
            assert len(data) == 1
            assert data[0]['id'] == 1

        if authorization == 2:
            assert len(data) == 1
            assert data[0]['id'] == 2

def test_customer_add():
    for user in users:
        username = user[0]
        password = user[1]
        authorization = user[2]

        res = requests.post(
            'http://127.0.0.1:8000/customers/',
            auth=HTTPBasicAuth(username, password),
        )
        data = res.json()
        if authorization == 4:
            assert data['email'][0] == 'Ce champ est obligatoire.'

        if authorization == 3:
            assert data['email'][0] == 'Ce champ est obligatoire.'

        if authorization == 2:
            assert data['detail'] == "Vous n'avez pas la permission d'effectuer cette action."

def test_customer_update():
    for user in users:
        username = user[0]
        password = user[1]
        authorization = user[2]

        res = requests.put(
            'http://127.0.0.1:8000/customers/1',
            auth=HTTPBasicAuth(username, password),
        )
        data = res.json()
        if authorization == 4:
            assert data['email'][0] == 'Ce champ est obligatoire.'

        if authorization == 3:
            assert data['email'][0] == 'Ce champ est obligatoire.'

        if authorization == 2:
            assert data['detail'] == "Vous n'avez pas la permission d'effectuer cette action."

def test_event_add():
    for user in users:
        username = user[0]
        password = user[1]
        authorization = user[2]

        res = requests.post(
            'http://127.0.0.1:8000/contracts/3/events/',
            auth=HTTPBasicAuth(username, password),
        )

        data = res.json()
        if authorization == 4:
            assert data['title'][0] == 'Ce champ est obligatoire.'

        if authorization == 3:
            assert data['title'][0] == 'Ce champ est obligatoire.'

        if authorization == 2:
            assert data['detail'] == "Vous n'avez pas la permission d'effectuer cette action."

def test_events_get_all():
    for user in users:
        username = user[0]
        password = user[1]
        authorization = user[2]

        res = requests.get(
            'http://127.0.0.1:8000/contracts/all/events/',
            auth=HTTPBasicAuth(username, password),
        )
        data = res.json()
        if authorization == 4:
            assert len(data) == 3

        if authorization == 3:
            assert data == []

        if authorization == 2:
            assert len(data) == 2

def test_event_update():
    for user in users:
        username = user[0]
        password = user[1]
        authorization = user[2]

        res = requests.put(
            'http://127.0.0.1:8000/contracts/5/events/3',
            auth=HTTPBasicAuth(username, password),
        )
        data = res.json()
        if authorization == 4:
            assert data['title'][0]

        if authorization == 3:
            assert data['detail'] == "Vous n'avez pas la permission d'effectuer cette action."

        if authorization == 2:
            assert data['title'][0]