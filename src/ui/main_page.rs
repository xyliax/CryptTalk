use crate::app::App;
use crate::ui::centered_rect;
use ratatui::{
    layout::{Alignment, Constraint, Direction, Layout, Rect},
    style::{Style, Stylize},
    widgets::{block::Title, Block, BorderType, Borders, Paragraph},
    Frame,
};

pub fn ui(f: &mut Frame, app: &App, center_chunk: &Rect, bottom_chunk: &Rect) {
    // main page
    let main_chunks = Layout::default()
        .direction(Direction::Vertical)
        .constraints([
            Constraint::Length(3),
            Constraint::Length(3),
            Constraint::Length(3),
            Constraint::Min(0),
        ])
        .split(centered_rect(100, 100, *center_chunk));
    // "MAIN PAGE"
    f.render_widget(
        Paragraph::new("MAIN PAGE".green().bold())
            .block(
                Block::default()
                    .title(Title::from("Where am I".blue()))
                    .title(Title::from("Welcome".blue()).alignment(Alignment::Center))
                    .borders(Borders::ALL)
                    .style(Style::default())
                    .blue()
                    .bold(),
            )
            .alignment(Alignment::Center),
        main_chunks[0],
    );
    // "REGISTER"
    f.render_widget(
        Paragraph::new("REGISTER".green().bold())
            .block(
                Block::default()
                    .title(Title::from("New User").alignment(Alignment::Left))
                    .title(Title::from("Press 'R'".blue()).alignment(Alignment::Center))
                    .borders(Borders::ALL)
                    .style(Style::default())
                    .blue()
                    .bold(),
            )
            .alignment(Alignment::Center),
        main_chunks[1],
    );
    // "LOGIN"
    f.render_widget(
        Paragraph::new("LOGIN".green().bold())
            .block(
                Block::default()
                    .title(Title::from("Has Account").alignment(Alignment::Left))
                    .title(Title::from("Press 'L'").alignment(Alignment::Center))
                    .borders(Borders::ALL)
                    .style(Style::default())
                    .blue()
                    .bold(),
            )
            .alignment(Alignment::Center),
        main_chunks[2],
    );
    // empty board
    f.render_widget(
        Block::default().borders(Borders::ALL).border_type(BorderType::Thick),
        main_chunks[3],
    );
    // bottom bar
    let logged_text = if app.logged {
        format!("Logged as {}", app.user.username).green()
    } else {
        "Not Logged In".red()
    };
    f.render_widget(
        Paragraph::new("Secured and Trustworthy".green().bold())
            .block(
                Block::default()
                    .title(Title::from(logged_text).alignment(Alignment::Left))
                    .title(Title::from("Status Bar".blue()).alignment(Alignment::Center))
                    .borders(Borders::ALL)
                    .border_type(BorderType::Rounded)
                    .style(Style::default())
                    .blue()
                    .bold(),
            )
            .alignment(Alignment::Center),
        *bottom_chunk,
    );
}
