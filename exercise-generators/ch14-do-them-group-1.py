#!/usr/bin/env bash
"""true" '''\'
set -e
eval "$(${CONDA_EXE:-conda} shell.bash hook)"
conda activate cherokee-lessons
exec python "$0" "$@"
exit $?
''"""
import os
import pathlib
import random
import re
import textwrap

output_lyx: str = "ch14-do-them-group-1.lyx"

raw_text: str = """
ᎤᏁᎦ ᏅᏯ.
ᎤᏬᏗᎨ ᏅᏯ.
ᎬᎿᎨ ᏅᏯ.
ᏓᎶᏂᎨ ᏅᏯ.
ᏓᎶᏂᎨ ᎤᏍᎪᎸ ᏅᏯ.
ᎢᏤᎢᏳᏍᏗ ᎩᏟ.
ᎤᏁᎦ ᎩᏟ [a].
ᎠᎩᎦᎨ ᎩᏟ.
ᎠᏓᎭᎵᎨ ᎩᏟ.
ᎠᏓᎶᏂᎨ ᎩᏟ.
ᎢᏤᎢᏳᏍᏗ ᏪᏌ [a].
ᎤᏬᏗᎨ ᏪᏌ [a].
ᎠᏌᎪᏂᎨ ᏪᏌ.
ᎠᏓᎭᎵᎨ ᏪᏌ.
ᎠᏓᎶᏂᎨ ᎤᏍᎪᎸ ᏪᏌ.
ᎤᏁᎦ ᎩᏟ [i].
ᎬᎿᎨ ᎩᏟ.
ᏌᎪᏂᎨ ᎩᏟ.
ᏓᎶᏂᎨ ᎩᏟ.
ᏓᎶᏂᎨ ᎤᏍᎪᎸ ᎩᏟ.
ᎢᏤᎢᏳᏍᏗ ᏪᏌ [i].
ᎤᏬᏗᎨ ᏪᏌ [i].
ᎩᎦᎨ ᏪᏌ.
ᎬᎿᎨ ᏪᏌ.
ᏓᎶᏂᎨ ᏪᏌ.
"""

plural_forms: set[str] = set()
plural_forms.add("ᎠᏂᏤᎢᏳᏍᏗ")
plural_forms.add("ᎤᏂᏁᎦ")
plural_forms.add("ᏧᏃᏗᎨ")
plural_forms.add("ᎠᏂᎬᎿᎨ")
plural_forms.add("ᎠᏂᏓᎶᏂᎨ")
plural_forms.add("ᏗᏤᎢᏳᏍᏗ")
plural_forms.add("ᏧᏁᎦ")
plural_forms.add("ᏧᏬᏗᎨ")
plural_forms.add("ᏗᎬᎿᎨ")
plural_forms.add("ᏗᏓᎶᏂᎨ")

multicolumn_begin: str = """
\\begin_layout Standard
\\begin_inset ERT
status collapsed

\\begin_layout Plain Layout


\\backslash
begin{multicols}{2}
\\end_layout

\\begin_layout Plain Layout


\\backslash
raggedcolumns
\\end_layout

\\end_inset


\\end_layout
"""

multicolumn_end: str = """
\\begin_layout Standard
\\begin_inset ERT
status collapsed

\\begin_layout Plain Layout


\\backslash
end{multicols}
\\end_layout

\\end_inset


\\end_layout
"""


def main() -> None:
    random.seed(0)
    wanted_sets: int = 5
    wanted_per_set: int = 4
    os.chdir(pathlib.Path(__file__).parent)
    entries: list[str] = list()
    for entry in textwrap.dedent(raw_text).split("\n"):
        entry = entry.strip()
        if not entry:
            continue
        if entry in entries:
            continue
        entries.append(entry)

    print(f"Have {len(entries):,} source entries.")

    jalagi_content: str = ""

    wanted: int = wanted_sets * wanted_per_set
    already: list[str] = list()
    print(f"Wanted: {wanted:,}")
    set_counter: int = 0
    item_counter: int = wanted_per_set
    while wanted > 0:
        entry: str = random.choice(entries)
        if entry in already:
            continue
        wanted -= 1
        item_counter += 1
        if item_counter >= wanted_per_set:
            item_counter = 0
            set_counter += 1
            if set_counter > 1:
                jalagi_content += "\n"
                jalagi_content += multicolumn_end
                jalagi_content += "\n"
            jalagi_content += "\\begin_layout Subsubsection*\n"
            jalagi_content += f"Set {set_counter:,}\n"
            jalagi_content += "\\end_layout\n"
            jalagi_content += "\n"
            jalagi_content += multicolumn_begin
            jalagi_content += "\n"
        already.append(entry)
        color_form: str = entry[:entry.replace(" [a]", "").replace(" [i]", "") .rindex(" ")]
        correct_answer: str = entry
        cards_to_show: list[str] = list()
        already_bad_colors: set[str] = set()
        while len(cards_to_show) < 3:
            maybe_incorrect: str = random.choice(entries)
            if maybe_incorrect.startswith(color_form):
                continue
            bad_color_form: str = maybe_incorrect[:maybe_incorrect.index(" ")]
            if bad_color_form in already_bad_colors:
                continue
            already_bad_colors.add(bad_color_form)
            cards_to_show.append(maybe_incorrect)
        cards_to_show.append(correct_answer)
        random.shuffle(cards_to_show)

        jalagi_content += "\\begin_layout Enumerate\n"
        jalagi_content += f"[Ꭰ] "
        card: str
        for card in cards_to_show:
            jalagi_content += f"{card} \n"
            jalagi_content += f" \n"

        jalagi_content += "\\begin_deeper\n"
        jalagi_content += "\\begin_layout Enumerate\n"
        question_text: str = f"[Ꭰ] ᎦᏙ ᎤᏍᏗ {color_form}?\n"
        for plural_form in plural_forms:
            if color_form.startswith(plural_form):
                question_text = f"[Ꭰ] ᎦᏙ ᎤᎾᏍᏗ {color_form}?\n"
                break
        jalagi_content += question_text
        jalagi_content += "\\end_layout\n"

        this_is_form = correct_answer[correct_answer.index(" ") + 1:]
        if this_is_form[-1] in ".!?,":
            this_is_form = this_is_form[:-1]

        this_is_form_item: str = correct_answer[:correct_answer.rindex(" ")]
        this_is_form += " " + this_is_form_item

        this_is_form = re.sub("\[.\]", "", this_is_form)
        this_is_form = re.sub(" +", " ", this_is_form).strip()

        jalagi_content += "\\begin_layout Enumerate\n"
        jalagi_content += f"[Ꭱ] ⇒ {correct_answer}\n"
        jalagi_content += "\\end_layout\n"

        jalagi_content += "\\begin_layout Enumerate\n"
        jalagi_content += f"[Ꭱ] ᎯᎠ {this_is_form}.\n"
        jalagi_content += "\\end_layout\n"

        jalagi_content += "\\end_deeper\n\n"
        jalagi_content += "\end_layout\n"

    jalagi_content += "\n"
    jalagi_content += multicolumn_end
    jalagi_content += "\n"

    with open("written-jalagi-gilisi-template.lyx") as r:
        lyx_content = r.read()
        lyx_content = re.sub("(?s)\\\\begin_layout Standard\\s+jalagi\\s+\\\\end_layout\\s+",
                             jalagi_content.replace("\\", "\\\\"), lyx_content)

    with open(output_lyx, "w") as w:
        w.write(lyx_content)


if __name__ == '__main__':
    main()
