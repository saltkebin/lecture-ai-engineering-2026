from types import SimpleNamespace

import app.ask as ask_module


def test_ask_prints_prompt_and_output_token_counts(monkeypatch, capsys):
    class FakeModels:
        @staticmethod
        def generate_content(model, contents):
            return SimpleNamespace(
                text="回答です",
                usage_metadata=SimpleNamespace(
                    prompt_token_count=123,
                    candidates_token_count=45,
                ),
            )

    class FakeClient:
        def __init__(self, api_key):
            self.api_key = api_key
            self.models = FakeModels()

    monkeypatch.setattr(ask_module, "get_api_key", lambda: "dummy-key")
    monkeypatch.setattr(ask_module.genai, "Client", FakeClient)

    answer = ask_module.ask("テスト質問")

    assert answer == "回答です"
    captured = capsys.readouterr().out
    assert "入力トークン数: 123" in captured
    assert "出力トークン数: 45" in captured
