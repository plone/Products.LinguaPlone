NAME=LinguaPlone
MAJOR_VERSION=0
MINOR_VERSION=9
RELEASE_TAG=.0
PACKAGE_NAME=${NAME}-${MAJOR_VERSION}.${MINOR_VERSION}${RELEASE_TAG}

PYTHON=/usr/bin/python
TMPDIR=/tmp

ZOPE=/usr/local/zope
SOFTWARE_HOME=${ZOPE}/Zope/2.8/Zope/lib/python
INSTANCE_HOME=${ZOPE}/instance/zope2.8-cmf1.5-plone2.1
BASE_DIR=${INSTANCE_HOME}/Products
CURDIR=${BASE_DIR}/${NAME}

RMRF=rm -rf
FIND=find
ECHO=echo -n
CD=cd
LN=ln -sfn
TAR=tar -czhf
MKDIR=mkdir -p

.PHONY: clean test reindent reindent_clean sdist
.PHONY: default

# The default step (invoked when make is called without a target)
default: clean test

clean:
	${FIND} . \( -name '*~' -o -name '*.py[co]' -o -name '*.bak' \) -exec rm {} \; -print

# Grab reindent.pt from Python Tools CVS:
# http://cvs.sourceforge.net/viewcvs.py/python/python/dist/src/Tools/scripts
reindent:
	~/scripts/reindent.py -r -v .

test:
	export INSTANCE_HOME=${INSTANCE_HOME}; \
	export SOFTWARE_HOME=${SOFTWARE_HOME}; \
	${PYTHON} ${CURDIR}/tests/runalltests.py

# Create a source distribution file (implies clean).
sdist: reindent clean sdist_tgz

# Create a tgz archive file as a source distribution.
sdist_tgz:
	${ECHO} "${MAJOR_VERSION}.${MINOR_VERSION}${RELEASE_TAG} - r" > \
		${CURDIR}/version.txt
	svnversion >> ${CURDIR}/version.txt
	${MKDIR} ${TMPDIR}/${PACKAGE_NAME}
	${CD} ${TMPDIR}/${PACKAGE_NAME} && \
		${LN} ${BASE_DIR}/${NAME} && \
		${CD} ${TMPDIR} && \
		${TAR} ${BASE_DIR}/${PACKAGE_NAME}.tgz \
			--exclude=.svn \
			--exclude=*.pyc \
			--exclude=*~ \
			--exclude=.#* \
			${PACKAGE_NAME}
	${RMRF} ${TMPDIR}/${PACKAGE_NAME}
