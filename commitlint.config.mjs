// Commit format: .agents/skills/yo-commit/SKILL.md
export default {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [2, 'always', ['feat', 'fix', 'refactor', 'test', 'docs', 'chore']],
    'scope-enum': [
      2,
      'always',
      ['catalogue', 'lists', 'accounts', 'api', 'db', 'data', 'mcp', 'ui', 'ci', 'agents', 'docs'],
    ],
    'header-max-length': [2, 'always', 72],
  },
};
