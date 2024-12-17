.PHONY: v%
v%:
	python3 -m build
	git add .
	git commit -m "Release version $*"
	git tag $@
	git push origin $@