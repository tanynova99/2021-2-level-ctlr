set -ex

echo -e '\n'
echo 'Running lint check...'

TARGET_SCORE_PIPELINE=$(bash config/get_mark.sh pipeline)
TARGET_SCORE_CRAWLER=$(bash config/get_mark.sh crawler)

LINT_SCORE=$(( TARGET_SCORE_CRAWLER > TARGET_SCORE_PIPELINE ? TARGET_SCORE_CRAWLER : TARGET_SCORE_PIPELINE))

source venv/bin/activate

lint_output=$(python -m pylint scrapper.py pipeline.py pos_frequency_pipeline.py constants.py core_utils config \
              --rcfile config/stage_1_style_tests/.pylintrc)

python config/stage_1_style_tests/lint_level.py \
          --lint-output "$lint_output" \
          --target-score "$LINT_SCORE"
