module.exports = {
    "root": true,
    "env": {
        "browser": true,
        "es2021": true,
        "node": true
    },
    "extends": [
        "eslint:recommended",
        "plugin:@typescript-eslint/recommended",
        "plugin:vue/vue3-essential",
        'plugin:prettier/recommended'
    ],
    "overrides": [
        {
            "env": {
                "node": true
            },
            "files": [
                ".eslintrc.{js,cjs}",
                'src/views/**/*.vue'
            ],
            "parserOptions": {
                "sourceType": "script"
            },
            rules: {
                'vue/multi-word-component-names': 0,
            },
        }
    ],
    "parserOptions": {
        "ecmaVersion": "latest",
        "parser": "@typescript-eslint/parser",
        "sourceType": "module"
    },
    "plugins": [
        "@typescript-eslint",
        "vue",
        "prettier"
    ],
    "rules": {
        'prettier/prettier': 'error',
        'vue/multi-word-component-names': 'off',
        '@typescript-eslint/no-explicit-any': 'warn'
    },
    "ignores":[
        "build/*.js",
        "src/assets",
        "node_modules",
        "public",
        "dist",
        "auto-import.d.ts",
        "components.d.ts"
    ]
}
