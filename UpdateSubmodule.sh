#!/bin/bash

# 推送主仓库的更改
git add .
git commit -m "Update main repository"
git push

# 遍历所有子模块并推送更改
git submodule foreach 'git add .; git commit -m "Update submodule"; git push'

echo "所有子模块已推送。"
