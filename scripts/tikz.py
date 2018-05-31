def __init__(self, print_sent_id=True, print_text=True, print_preambule=True,
	attributes='form,upos', **kwargs):
	"""Create the Tikz block object.
	Args:
	print_sent_id: print sent_id (`tree.address()`) as a LaTeX comment (default=True)
	print_text: print sentence text  (`tree.get_sentence()`) as a LaTeX comment (default=True)
	print_preambule: surround each document with LaTeX preambule (`documentclass` etc)
		 and `end{document}` (default=True)
	attributes: comma-separated list of node attributes to print (each on a separate line).
        """
        super().__init__(**kwargs)
        self.print_sent_id = print_sent_id
        self.print_text = print_text
        self.print_preambule = print_preambule
        self.node_attributes = attributes.split(',')

def before_process_document(self, doc):
        super().before_process_document(doc)
        if self.print_preambule:
            print(r'\documentclass{article}')
            print(r'\usepackage[T1]{fontenc}')
            print(r'\usepackage[utf8]{inputenc}')
            print(r'\usepackage{tikz-dependency}')
            print(r'\begin{document}')

def after_process_document(self, doc):
        if self.print_preambule:
            print(r'\end{document}')
        logging.info('Use pdflatex to compile the output')
        super().after_process_document(doc)

def process_tree(self, tree):
        print(r'\begin{dependency}')
        print(r'\begin{deptext}')
        nodes = tree.descendants

        if self.print_sent_id:
            print('% sent_id = ' + tree.address())

        if self.print_text:
            print("% text = " + tree.get_sentence())

        comment = tree.comment
        if comment:
            comment = comment.rstrip()
            print('%' + comment.replace('\n', '\n%'))

        lines = ['' for _ in self.node_attributes]
        for node in nodes:
            values = [str(getattr(node, attr_name)) for attr_name in self.node_attributes]
            values = [v if v != '_' else r'\_' for v in values]
            max_len = max(len(value) for value in values)
            for index, value in enumerate(values):
                if node.ord > 1:
                    lines[index] += r' \& '
                lines[index] += value.ljust(max_len)
        for line in lines:
            print(line + r' \\')
        print(r'\end{deptext}')
        for node in nodes:
            if node.parent.is_root():
                print(r'\deproot{%d}{root}' % node.ord)
            else:
                print(r'\depedge{%d}{%d}{%s}' % (node.parent.ord, node.ord, node.deprel))
        print(r'\end{dependency}')
        print('')
