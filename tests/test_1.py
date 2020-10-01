import json


def test_index(app,client):
    res = client.get('/')
    assert res.status_code == 200
    data = res.get_data(as_text=True)
    print('checking data >>>')
    print(data)
    print('<<< checking end')
    assert data

