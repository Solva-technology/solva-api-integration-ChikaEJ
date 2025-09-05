from unittest.mock import patch

from app.handlers.rps import play_rps


def test_play_draw():
    with patch("app.handlers.rps.random.choice", return_value="Камень"):
        result = play_rps("rock")
        assert "Ничья 🤝" in result
        assert "Ваш выбор: Камень" in result
        assert "Компьютер выбрал: Камень" in result


def test_play_win():
    with patch("app.handlers.rps.random.choice", return_value="Ножницы"):
        result = play_rps("rock")
        assert "Вы выиграли 🎉" in result
        assert "Компьютер выбрал: Ножницы" in result


def test_play_lose():
    with patch("app.handlers.rps.random.choice", return_value="Бумага"):
        result = play_rps("rock")
        assert "Вы проиграли 😢" in result
        assert "Ваш выбор: Камень" in result
