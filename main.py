import tkinter as tk
from tkinter import messagebox

class NoteApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Aplicativo de Notas")
        
        # Variável para armazenar a lista de notas
        self.notes = []

        # Configuração da interface
        self.setup_ui()

    def setup_ui(self):
        # Frame para a lista de notas
        self.list_frame = tk.Frame(self.master)
        self.list_frame.pack(pady=10)

        # Lista de notas
        self.note_listbox = tk.Listbox(self.list_frame, width=50)
        self.note_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar para a lista de notas
        self.scrollbar = tk.Scrollbar(self.list_frame, orient=tk.VERTICAL, command=self.note_listbox.yview)
        self.note_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Frame para os botões
        self.button_frame = tk.Frame(self.master)
        self.button_frame.pack(pady=10)

        # Botões para adicionar, editar e excluir notas
        self.add_button = tk.Button(self.button_frame, text="Adicionar Nota", command=self.add_note)
        self.add_button.grid(row=0, column=0, padx=5)

        self.edit_button = tk.Button(self.button_frame, text="Editar Nota", command=self.edit_note)
        self.edit_button.grid(row=0, column=1, padx=5)

        self.delete_button = tk.Button(self.button_frame, text="Excluir Nota", command=self.delete_note)
        self.delete_button.grid(row=0, column=2, padx=5)

        # Carregar notas existentes (se houver)
        self.load_notes()

    def load_notes(self):
        # Carregar notas do arquivo (se existir)
        try:
            with open("notes.txt", "r") as file:
                self.notes = [line.strip() for line in file.readlines()]
                self.display_notes()
        except FileNotFoundError:
            pass

    def display_notes(self):
        # Limpar a lista de notas
        self.note_listbox.delete(0, tk.END)

        # Adicionar notas à lista de notas
        for note in self.notes:
            self.note_listbox.insert(tk.END, note)

    def add_note(self):
        # Abrir uma nova janela para adicionar uma nota
        add_window = tk.Toplevel()
        add_window.title("Adicionar Nota")

        # Campo de texto para a nova nota
        note_entry = tk.Text(add_window, height=10, width=50)
        note_entry.pack(pady=10)

        # Botão para adicionar a nota
        add_button = tk.Button(add_window, text="Adicionar", command=lambda: self.save_note(add_window, note_entry))
        add_button.pack()

    def save_note(self, add_window, note_entry):
        # Obter o conteúdo da nota
        note_content = note_entry.get("1.0", tk.END).strip()

        if note_content:
            # Adicionar a nota à lista de notas
            self.notes.append(note_content)
            self.display_notes()

            # Salvar a nota no arquivo
            self.save_notes_to_file()

            # Fechar a janela de adicionar nota
            add_window.destroy()
        else:
            messagebox.showwarning("Aviso", "Por favor, insira algum conteúdo para a nota.")

    def edit_note(self):
        # Verificar se uma nota foi selecionada
        if self.note_listbox.curselection():
            # Obter o índice da nota selecionada
            index = self.note_listbox.curselection()[0]
            selected_note = self.notes[index]

            # Abrir uma nova janela para editar a nota selecionada
            edit_window = tk.Toplevel()
            edit_window.title("Editar Nota")

            # Campo de texto para editar a nota
            edit_entry = tk.Text(edit_window, height=10, width=50)
            edit_entry.insert(tk.END, selected_note)
            edit_entry.pack(pady=10)

            # Botão para salvar a nota editada
            save_button = tk.Button(edit_window, text="Salvar", command=lambda: self.save_edit(edit_window, index, edit_entry))
            save_button.pack()
        else:
            messagebox.showwarning("Aviso", "Por favor, selecione uma nota para editar.")

    def save_edit(self, edit_window, index, edit_entry):
        # Obter o conteúdo da nota editada
        edited_note = edit_entry.get("1.0", tk.END).strip()

        if edited_note:
            # Atualizar a nota na lista de notas
            self.notes[index] = edited_note
            self.display_notes()

            # Salvar as notas no arquivo
            self.save_notes_to_file()

            # Fechar a janela de edição
            edit_window.destroy()
        else:
            messagebox.showwarning("Aviso", "Por favor, insira algum conteúdo para a nota.")

    def delete_note(self):
        # Verificar se uma nota foi selecionada
        if self.note_listbox.curselection():
            # Obter o índice da nota selecionada
            index = self.note_listbox.curselection()[0]

            # Remover a nota da lista de notas
            del self.notes[index]
            self.display_notes()

            # Salvar as notas no arquivo
            self.save_notes_to_file()
        else:
            messagebox.showwarning("Aviso", "Por favor, selecione uma nota para excluir.")

    def save_notes_to_file(self):
        # Salvar as notas no arquivo
        with open("notes.txt", "w") as file:
            for note in self.notes:
                file.write(note + "\n")

def main():
    root = tk.Tk()
    note_app = NoteApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
