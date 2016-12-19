# The Makefile is based on the sample sphinx make, but modified for our needs
#

# You can set these variables from the command line.
SPHINXOPTS    =
SOURCEDIR     = .

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	SDK_LANG="python" sphinx-build -M $@ "$(SOURCEDIR)" "_python" $(SPHINXOPTS) $(O)
	SDK_LANG="go" sphinx-build -M $@ "$(SOURCEDIR)" "_go" $(SPHINXOPTS) $(O)
