import React, { useEffect, useState } from "react";
import styled from "styled-components";
import { Button, Input, Textarea, Box } from "../styles";

const NotesListStyled = styled.ul`
  list-style: none;
  padding: 0;
`;

const NoteItem = styled.li`
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 16px;
  background: white;

  h3 {
    margin: 0 0 8px 0;
  }

  p {
    margin: 0 0 16px 0;
  }
`;

function NotesList({ token }) {
  const [notes, setNotes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [editNote, setEditNote] = useState(null); // note being edited

  const fetchNotes = () => {
    fetch("/notes", {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((r) => r.json())
      .then((data) => {
        setNotes(data.notes);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  };

  useEffect(() => {
    fetchNotes();
  }, [token]);

  const handleCreate = (e) => {
    e.preventDefault();
    fetch("/notes", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ title, content }),
    })
      .then((r) => r.json())
      .then(() => {
        setTitle("");
        setContent("");
        setShowForm(false);
        fetchNotes(); // refresh list
        alert("Note created successfully!");
      });
  };

  const handleEdit = (e) => {
    e.preventDefault();
    fetch(`/notes/${editNote.id}`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ title, content }),
    })
      .then((r) => r.json())
      .then(() => {
        setEditNote(null);
        setTitle("");
        setContent("");
        fetchNotes(); // refresh list
        alert("Note updated successfully!");
      });
  };

  const handleDelete = (id) => {
    if (window.confirm("Are you sure you want to delete this note?")) {
      fetch(`/notes/${id}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` },
      }).then(() => {
        fetchNotes();
        alert("Note deleted successfully!");
      });
    }
  };

  const openEdit = (note) => {
    setEditNote(note);
    setTitle(note.title);
    setContent(note.content);
    setShowForm(false);
  };

  if (loading) return <p>Loading notes...</p>;

  return (
    <Box>
      {/* Create Note button */}
      <Button onClick={() => { setShowForm(!showForm); setEditNote(null); }}>
        + Create Note
      </Button>

      {/* Create form */}
      {showForm && (
        <Box as="form" onSubmit={handleCreate}>
          <Input
            placeholder="Title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
          />
          <Textarea
            placeholder="Content"
            value={content}
            onChange={(e) => setContent(e.target.value)}
            required
          />
          <Button type="submit">Save Note</Button>
          <Button variant="outline" type="button" onClick={() => setShowForm(false)}>Cancel</Button>
        </Box>
      )}

      {/* Edit form */}
      {editNote && (
        <Box as="form" onSubmit={handleEdit}>
          <Input
            placeholder="Title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
          />
          <Textarea
            placeholder="Content"
            value={content}
            onChange={(e) => setContent(e.target.value)}
            required
          />
          <Button type="submit">Update Note</Button>
          <Button variant="outline" type="button" onClick={() => setEditNote(null)}>Cancel</Button>
        </Box>
      )}

      {/* Notes list */}
      {notes.length === 0 ? (
        <p>No notes yet. Create one!</p>
      ) : (
        <NotesListStyled>
          {notes.map((note) => (
            <NoteItem key={note.id}>
              <h3>{note.title}</h3>
              <p>{note.content}</p>
              <Button variant="outline" onClick={() => openEdit(note)}>Edit</Button>
              <Button variant="outline" color="danger" onClick={() => handleDelete(note.id)}>Delete</Button>
            </NoteItem>
          ))}
        </NotesListStyled>
      )}
    </Box>
  );
}

export default NotesList;