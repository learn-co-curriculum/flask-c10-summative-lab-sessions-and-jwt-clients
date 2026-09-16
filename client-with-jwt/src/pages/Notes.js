import { useState, useEffect } from "react";
import styled from "styled-components";
import { Button, Input, FormField, Label, Textarea } from "../styles";
import { apiFetch } from "../api";

const categories = ["Notes", "Tasks", "Workouts", "Journal"];

function NotesPage({ user }) {
  const [notes, setNotes] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState("Notes");
  const [selectedId, setSelectedId] = useState(null);
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [page, setPage] = useState(1);
  const [lastPage, setLastPage] = useState(1);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const token = localStorage.getItem("token");

  function fetchNotes(nextPage = 1, category = selectedCategory) {
    setLoading(true);
    apiFetch(`/notes?page=${nextPage}&per_page=3&category=${encodeURIComponent(category)}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then((r) => {
        if (!r.ok) throw new Error("Unable to load notes");
        return r.json();
      })
      .then((data) => {
        setNotes(data.items || []);
        setPage(data.page || 1);
        setLastPage(data.pages || 1);
        setLoading(false);
      })
      .catch(() => {
        setError("Could not load notes.");
        setLoading(false);
      });
  }

  useEffect(() => {
    fetchNotes(1, selectedCategory);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedCategory]);

  function resetForm() {
    setSelectedId(null);
    setTitle("");
    setContent("");
  }

  function handleEdit(note) {
    setSelectedId(note.id);
    setSelectedCategory(note.category || "Notes");
    setTitle(note.title);
    setContent(note.content);
  }

  function handleSubmit(e) {
    e.preventDefault();
    setError("");

    if (!title.trim() || !content.trim()) {
      setError("Title and content are required.");
      return;
    }

    const payload = {
      title: title.trim(),
      content: content.trim(),
      category: selectedCategory,
    };

    const request = selectedId
      ? apiFetch(`/notes/${selectedId}`, {
          method: "PATCH",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify(payload),
        })
      : apiFetch("/notes", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify(payload),
        });

    request
      .then((r) => {
        if (!r.ok) throw new Error("Unable to save note");
        return r.json();
      })
      .then(() => {
        resetForm();
        fetchNotes(page, selectedCategory);
      })
      .catch(() => {
        setError("Could not save this note.");
      });
  }

  function handleDelete(id) {
    if (!window.confirm("Delete this entry?")) return;

    apiFetch(`/notes/${id}`, {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then((r) => {
        if (!r.ok) throw new Error("Delete failed");
        return r.json();
      })
      .then(() => {
        resetForm();
        fetchNotes(page, selectedCategory);
      })
      .catch(() => {
        setError("Could not delete this note.");
      });
  }

  return (
    <Page>
      <Header>
        <div>
          <Eyebrow>Welcome, {user?.username}</Eyebrow>
          <Title>My Productivity Board</Title>
        </div>
      </Header>

      <CategoryBar>
        {categories.map((category) => (
          <CategoryButton
            key={category}
            type="button"
            active={selectedCategory === category}
            onClick={() => setSelectedCategory(category)}
          >
            {category}
          </CategoryButton>
        ))}
      </CategoryBar>

      <Grid>
        <Panel>
          <PanelTitle>{selectedId ? "Edit entry" : "New entry"}</PanelTitle>
          <form onSubmit={handleSubmit}>
            <FormField>
              <Label>Category</Label>
              <Select value={selectedCategory} onChange={(e) => setSelectedCategory(e.target.value)}>
                {categories.map((category) => (
                  <option key={category} value={category}>
                    {category}
                  </option>
                ))}
              </Select>
            </FormField>
            <FormField>
              <Label>Title</Label>
              <Input
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
              />
            </FormField>
            <FormField>
              <Label>Content</Label>
              <Textarea
                rows="5"
                value={content}
                onChange={(e) => setContent(e.target.value)}
              />
            </FormField>
            {error ? <ErrorText>{error}</ErrorText> : null}
            <ActionRow>
              <Button type="submit">{selectedId ? "Update" : "Create"}</Button>
              {selectedId ? (
                <Button variant="outline" type="button" onClick={resetForm}>
                  Cancel
                </Button>
              ) : null}
            </ActionRow>
          </form>
        </Panel>

        <Panel>
          <PanelTitle>{selectedCategory}</PanelTitle>
          {loading ? <Muted>Loading entries...</Muted> : null}
          {!loading && notes.length === 0 ? (
            <Muted>No entries in this category yet.</Muted>
          ) : null}
          {!loading &&
            notes.map((note) => (
              <NoteCard key={note.id}>
                <NoteMeta>
                  <strong>{note.title}</strong>
                  <span>{note.category || "Notes"}</span>
                </NoteMeta>
                <NoteContent>{note.content}</NoteContent>
                <NoteActions>
                  <Button variant="outline" type="button" onClick={() => handleEdit(note)}>
                    Edit
                  </Button>
                  <Button type="button" onClick={() => handleDelete(note.id)}>
                    Delete
                  </Button>
                </NoteActions>
              </NoteCard>
            ))}

          <Pagination>
            <Button type="button" variant="outline" disabled={page <= 1} onClick={() => fetchNotes(page - 1, selectedCategory)}>
              Previous
            </Button>
            <PageLabel>
              Page {page} / {lastPage}
            </PageLabel>
            <Button type="button" variant="outline" disabled={page >= lastPage} onClick={() => fetchNotes(page + 1, selectedCategory)}>
              Next
            </Button>
          </Pagination>
        </Panel>
      </Grid>
    </Page>
  );
}

const Page = styled.div`
  max-width: 1100px;
  margin: 24px auto;
  padding: 0 16px 40px;
`;

const Header = styled.header`
  margin: 18px 0 16px;
  padding: 18px 20px 14px;
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.18);
  border: 1px solid rgba(255, 255, 255, 0.32);
  box-shadow: 0 10px 20px rgba(82, 28, 90, 0.08);
  backdrop-filter: blur(10px);
`;

const Eyebrow = styled.p`
  margin: 0 0 6px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-size: 12px;
  color: #4d2458;
  font-weight: 700;
`;

const Title = styled.h2`
  margin: 0;
  font-size: clamp(2rem, 3vw, 3rem);
  color: #3b194a;
  line-height: 1.1;
`;

const CategoryBar = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin: 16px 0 24px;
`;

const CategoryButton = styled.button`
  border: 1px solid rgba(255, 79, 163, 0.25);
  background: ${(props) => (props.active ? "linear-gradient(135deg, #ff4fa3 0%, #ff8ac4 100%)" : "rgba(255,255,255,0.7)")};
  color: ${(props) => (props.active ? "#fff" : "#5b1a3a")};
  padding: 9px 16px;
  border-radius: 999px;
  cursor: pointer;
  font-weight: 700;
  box-shadow: ${(props) => (props.active ? "0 10px 22px rgba(255,79,163,0.25)" : "none")};
`;

const Grid = styled.div`
  display: grid;
  grid-template-columns: 360px 1fr;
  gap: 20px;

  @media (max-width: 800px) {
    grid-template-columns: 1fr;
  }
`;

const Panel = styled.section`
  background: rgba(255, 255, 255, 0.78);
  border: 1px solid rgba(255, 255, 255, 0.4);
  border-radius: 18px;
  padding: 18px;
  box-shadow: 0 14px 28px rgba(122, 40, 92, 0.08);
`;

const PanelTitle = styled.h3`
  margin: 0 0 16px;
  font-size: 1.3rem;
  color: #5b1a3a;
`;

const ActionRow = styled.div`
  display: flex;
  gap: 10px;
  margin-top: 12px;
`;

const ErrorText = styled.p`
  color: #b42318;
  margin: 8px 0 0;
`;

const Muted = styled.p`
  color: #7a4861;
  margin: 0;
`;

const NoteCard = styled.article`
  border: 1px solid rgba(255, 79, 163, 0.18);
  border-radius: 14px;
  padding: 14px;
  margin-bottom: 12px;
  background: rgba(255, 245, 250, 0.9);
`;

const NoteMeta = styled.div`
  display: flex;
  justify-content: space-between;
  gap: 8px;
  margin-bottom: 8px;
  align-items: center;
  color: #5b1a3a;
`;

const NoteContent = styled.p`
  margin: 0 0 12px;
  white-space: pre-wrap;
  line-height: 1.6;
  color: #4a2a39;
`;

const NoteActions = styled.div`
  display: flex;
  justify-content: flex-end;
  gap: 8px;
`;

const Pagination = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 20px;
  gap: 10px;
`;

const PageLabel = styled.span`
  font-weight: 700;
  color: #5b1a3a;
`;

const Select = styled.select`
  display: block;
  width: 100%;
  padding: 10px 12px;
  border: 1px solid rgba(255, 79, 163, 0.2);
  border-radius: 10px;
  font-size: 1rem;
  background: rgba(255, 255, 255, 0.85);
`;

export default NotesPage;
