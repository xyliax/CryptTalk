mod login_page;
mod main_page;
mod register_page;
mod title_area;
mod tools;
use crate::app::{App, CurrentScreen};
use ratatui::{
    layout::{Constraint, Direction, Layout},
    Frame,
};
use tools::centered_rect;

pub fn ui(f: &mut Frame, app: &App) {
    let chunks = Layout::default()
        .direction(Direction::Vertical)
        .constraints([Constraint::Length(3), Constraint::Min(12), Constraint::Length(3)])
        .split(f.size());
    let (title_chunk, center_chunk, bottom_chunk) = (chunks[0], chunks[1], chunks[2]);

    title_area::ui(f, app, &title_chunk);

    match app.current_screen {
        CurrentScreen::Main => {
            main_page::ui(f, app, &center_chunk, &bottom_chunk);
        }
        CurrentScreen::Login => {
            login_page::ui(f, app, &center_chunk, &bottom_chunk);
        }
        CurrentScreen::Register => {
            register_page::ui(f, app, &center_chunk, &bottom_chunk);
        }
        CurrentScreen::Chat => {
            // chat page
        }
    }
}
