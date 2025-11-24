import pandas as pd
import matplotlib
matplotlib.use('Agg')

from src.eda import NewsEDA


def test_load_and_basic_info(tmp_path, capsys):
    """Test that load_data reads a CSV and basic_info prints expected text."""
    csv = tmp_path / "sample.csv"
    csv.write_text(
        "date,headline,publisher\n2020-01-01,First headline,PubA\n2020-01-02,Second headline,PubB\n2020-01-03,Third headline,PubA\n"
    )

    eda = NewsEDA(str(csv))
    df = eda.load_data()

    assert df is not None
    assert len(df) == 3
    assert 'headline' in df.columns

    # basic_info should run and print Columns
    eda.basic_info()
    captured = capsys.readouterr()
    assert 'Columns:' in captured.out


def test_news_description_runs(tmp_path):
    """Ensure news_description runs without raising (plots use Agg backend)."""
    csv = tmp_path / "sample2.csv"
    pd.DataFrame({
        'date': ['2020-01-01', '2020-01-02'],
        'headline': ['A', 'B'],
        'publisher': ['X', 'Y']
    }).to_csv(csv, index=False)

    eda = NewsEDA(str(csv))
    df = eda.load_data()
    # Should not raise
    eda.news_description()
