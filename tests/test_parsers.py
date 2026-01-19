from trading_journal.data.parsers import parse_money_es_co

def test_parse_money_basic():
    assert parse_money_es_co("$ 1.234,56") == 1234.56
    assert parse_money_es_co("- 2,90") == -2.90
    assert parse_money_es_co("-$108,40") == -108.40
