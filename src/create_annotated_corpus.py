import pandas as pd
import re
import os


if __name__ == '__main__':
    splits = ['train', 'valid', 'test_common', 'test_unseen']

    data = {split: pd.read_csv(f'data/cornell_rich_{split}.csv') for split in splits}

    os.makedirs("cornell_rich", exist_ok=True)
    os.makedirs("cornell_rich/context", exist_ok=True)

    for split in splits:
        c = pd.read_csv(f'data/cornell_rich_{split}.csv')
        # Replace nans with empty strings
        c = c.fillna('')
        for col in c.columns:
            if col in ['title_year', 'spoken_to_id', 'speaker_id', 'annotated.speaker', 'annotated.spoken_to',
                       'name.speaker', 'name.spoken_to']:
                continue
            data = c[col].tolist()
            filename = f"cornell_rich/context/{split}.{col}" if col != "utterance" else f"cornell_rich/{split}.en"
            if not filename.endswith(".speaker") and not filename.endswith(".spoken_to") and not filename.endswith(
                    ".en"):
                filename += ".meta"
            with open(filename, 'w+') as f:
                for line in data:
                    line = re.sub('Unknown', '', line)
                    f.write(repr(line)[1:-1] + "\n")
