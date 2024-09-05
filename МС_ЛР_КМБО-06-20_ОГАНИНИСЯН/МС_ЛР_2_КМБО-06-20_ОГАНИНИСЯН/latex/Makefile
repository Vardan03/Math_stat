all: build 

build: 
	latexmk -xelatex 
		 -synctex=1 main.tex

run:
	zathura main.pdf 

clean:
		rm *.aux \
		*.fdb_latexmk \
		*.fls \
		*.log \
		*.out \
		*.synctex.gz \
		*.toc \
		*.xdv
