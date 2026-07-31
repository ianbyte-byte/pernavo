#!/usr/bin/env bash
set -euo pipefail

validation_repo_root="$(cd "$(dirname "$0")/.." && pwd)"
validation_skill_root="$validation_repo_root/skills"
validation_corpus="$validation_repo_root/tests/skill-trigger-corpus.tsv"
validation_summarizer="$validation_repo_root/scripts/summarize-skill-trigger-results.py"
validation_cli_output="$(mktemp "${TMPDIR:-/tmp}/pernavo-skills-list.XXXXXX")"

cleanup_validation_output() {
  case "$validation_cli_output" in
    "${TMPDIR:-/tmp}"/pernavo-skills-list.*)
      rm -f -- "$validation_cli_output"
      ;;
    *)
      printf 'Refusing to remove unexpected temporary path: %s\n' "$validation_cli_output" >&2
      ;;
  esac
}
trap cleanup_validation_output EXIT

validation_validator="${PERNAVO_SKILL_VALIDATOR:-}"
if [[ -z "$validation_validator" ]]; then
  validation_legacy_validator="${LOONGCLAUDE_SKILL_VALIDATOR:-}"
  validation_validator="$validation_legacy_validator"
fi
if [[ -z "$validation_validator" ]]; then
  validation_codex_root="${CODEX_HOME:-${HOME}/.codex}"
  validation_validator="$validation_codex_root/skills/.system/skill-creator/scripts/quick_validate.py"
fi
if [[ ! -f "$validation_validator" ]]; then
  printf 'quick_validate.py not found: %s\n' "$validation_validator" >&2
  printf 'Set PERNAVO_SKILL_VALIDATOR to its absolute path.\n' >&2
  exit 1
fi

validation_skill_count=0
while IFS= read -r validation_skill_file; do
  validation_skill_dir="$(dirname "$validation_skill_file")"
  python3 "$validation_validator" "$validation_skill_dir"
  validation_skill_count=$((validation_skill_count + 1))
done < <(find "$validation_skill_root" -mindepth 2 -maxdepth 2 -type f -name SKILL.md | sort)

if [[ "$validation_skill_count" -eq 0 ]]; then
  printf 'No skills found under %s\n' "$validation_skill_root" >&2
  exit 1
fi

python3 - "$validation_summarizer" <<'PY'
import pathlib
import sys

path = pathlib.Path(sys.argv[1])
compile(path.read_text(encoding="utf-8"), str(path), "exec")
PY

ruby - "$validation_repo_root" "$validation_corpus" <<'RUBY'
require "csv"
require "pathname"
require "yaml"

repo_root = Pathname(ARGV.fetch(0))
corpus_path = Pathname(ARGV.fetch(1))
skill_files = Dir[repo_root.join("skills/*/SKILL.md").to_s].sort
skill_names = skill_files.map { |file| File.basename(File.dirname(file)) }

skill_files.each do |file|
  text = File.read(file)
  match = text.match(/\A---\s*\n(.*?)\n---\s*\n/m)
  abort("missing frontmatter: #{file}") unless match
  metadata = YAML.safe_load(match[1], permitted_classes: [], aliases: false)
  expected_name = File.basename(File.dirname(file))
  abort("name mismatch: #{file}") unless metadata["name"] == expected_name
  unsupported = metadata.keys - %w[name description]
  abort("unsupported frontmatter keys #{unsupported.inspect}: #{file}") unless unsupported.empty?
end

Dir[repo_root.join("skills/**/*.md").to_s].sort.each do |file|
  text = File.read(file)
  text.scan(/\[[^\]]*\]\(([^)]+)\)/).flatten.each do |raw_target|
    target = raw_target.strip.sub(/\A</, "").sub(/>\z/, "").split("#", 2).first
    next if target.nil? || target.empty? || target.match?(/\A[a-z][a-z0-9+.-]*:/i)
    resolved = Pathname(File.expand_path(target, File.dirname(file)))
    abort("broken relative link #{raw_target.inspect}: #{file}") unless resolved.exist?
  end
end

readme = File.read(repo_root.join("README.md"))
skill_names.each do |name|
  abort("README missing skill: #{name}") unless readme.include?("`#{name}`")
  installed_copy = repo_root.join(".agents/skills", name, "SKILL.md")
  abort("self-installed skill copy competes with source: #{installed_copy}") if installed_copy.exist?
end

lock_path = repo_root.join("skills-lock.json")
if lock_path.exist?
  lock_text = File.read(lock_path)
  legacy_lock_sources = ["tuloong/loongclaude"]
  self_reference_sources = ["tuloong/pernavo"] + legacy_lock_sources
  lock_source = self_reference_sources.find do |source|
    lock_text.include?(source)
  end
  abort("skills-lock.json self-references #{lock_source}") if lock_source
end

rows = CSV.read(corpus_path, headers: true, col_sep: "\t")
required_headers = %w[id subject expected forbidden prompt]
abort("unexpected corpus headers") unless rows.headers == required_headers
abort("expected three cases per skill") unless rows.length == skill_names.length * 3
abort("duplicate corpus ids") unless rows.map { |row| row["id"] }.uniq.length == rows.length

known_tokens = skill_names + ["-"]
rows.each do |row|
  abort("unknown corpus subject: #{row['subject']}") unless skill_names.include?(row["subject"])
  abort("empty corpus prompt: #{row['id']}") if row["prompt"].to_s.strip.empty?
  %w[expected forbidden].each do |column|
    row[column].split(",").each do |token|
      abort("unknown #{column} token #{token}: #{row['id']}") unless known_tokens.include?(token)
    end
  end
end

skill_names.each do |name|
  subject_rows = rows.select { |row| row["subject"] == name }
  case_types = subject_rows.map { |row| row["id"].split("_").last }.sort
  abort("missing positive/negative/collision cases for #{name}") unless case_types == %w[collision negative positive]
end

puts "#{skill_names.length} frontmatters, links, README entries, and trigger triplets valid"
RUBY

(
  cd "$validation_repo_root"
  NO_COLOR=1 npx --yes skills add . --list >"$validation_cli_output"
)
while IFS= read -r validation_skill_file; do
  validation_skill_name="$(basename "$(dirname "$validation_skill_file")")"
  if ! grep -Fq "$validation_skill_name" "$validation_cli_output"; then
    printf 'Skills CLI did not list: %s\n' "$validation_skill_name" >&2
    exit 1
  fi
done < <(find "$validation_skill_root" -mindepth 2 -maxdepth 2 -type f -name SKILL.md | sort)

git -C "$validation_repo_root" diff --check
printf 'PASS: %s skills validated and listed; corpus has %s cases.\n' \
  "$validation_skill_count" "$((validation_skill_count * 3))"
