use crate::app::{App, Mode};
use crate::ui::centered_rect;
use ratatui::{
    layout::{Alignment, Constraint, Direction, Layout, Rect},
    style::{Color, Style, Stylize},
    widgets::{block::Title, Block, BorderType, Borders, Paragraph},
    Frame,
};

pub fn ui(f: &mut Frame, app: &App, center_chunk: &Rect, bottom_chunk: &Rect) {
    // register page
    let main_chunks = Layout::default()
        .direction(Direction::Vertical)
        .constraints([
            Constraint::Length(3), // "REGISTER PAGE"
            Constraint::Length(2), // empty space
            Constraint::Length(3), // "USERNAME"
            Constraint::Length(3), // "EMAIL"
            Constraint::Length(3), // "PASSWORD"
            Constraint::Length(3), // "PASSWORD CONFIRM"
            Constraint::Length(2), // empty space
            Constraint::Length(3), // login button
            Constraint::Min(0),
        ])
        .split(centered_rect(100, 100, *center_chunk));
    // "REGISTER PAGE"
    f.render_widget(
        Paragraph::new("REGISTER PAGE".green().bold())
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
    // "USERNAME"
    let (title, border, switch_title) = {
        if app.mode == Mode::InputUsername {
            (Title::from("Typing"), BorderType::Thick, Title::from("Press ↑↓"))
        } else {
            (Title::from(""), BorderType::Plain, Title::from(""))
        }
    };
    f.render_widget(
        Paragraph::new(app.input_buffer.username.clone().green().bold())
            .block(
                Block::default()
                    .title(Title::from("USERNAME").alignment(Alignment::Left))
                    .title(title.alignment(Alignment::Center))
                    .title(switch_title.alignment(Alignment::Right))
                    .borders(Borders::ALL)
                    .border_type(border)
                    .style(Style::default())
                    .blue()
                    .bold(),
            )
            .alignment(Alignment::Center),
        centered_rect(60, 100, main_chunks[2]),
    );
    // "EMAIL"
    let (title, border, switch_title) = {
        if app.mode == Mode::InputEmail {
            (Title::from("Typing"), BorderType::Thick, Title::from("Press ↑↓"))
        } else {
            (Title::from(""), BorderType::Plain, Title::from(""))
        }
    };
    f.render_widget(
        Paragraph::new(app.input_buffer.username.clone().green().bold())
            .block(
                Block::default()
                    .title(Title::from("EMAIL").alignment(Alignment::Left))
                    .title(title.alignment(Alignment::Center))
                    .title(switch_title.alignment(Alignment::Right))
                    .borders(Borders::ALL)
                    .border_type(border)
                    .style(Style::default())
                    .blue()
                    .bold(),
            )
            .alignment(Alignment::Center),
        centered_rect(60, 100, main_chunks[3]),
    );
    // "PASSWORD"
    let (title, border, switch_title) = {
        if app.mode == Mode::InputPassword {
            (Title::from("Typing"), BorderType::Thick, Title::from("Press ↑↓"))
        } else {
            (Title::from(""), BorderType::Plain, Title::from(""))
        }
    };
    f.render_widget(
        Paragraph::new(
            std::iter::repeat('*')
                .take(app.input_buffer.password.len())
                .collect::<String>()
                .black()
                .bold(),
        )
        .block(
            Block::default()
                .title(Title::from("PASSWORD").alignment(Alignment::Left))
                .title(title.alignment(Alignment::Center))
                .title(switch_title.alignment(Alignment::Right))
                .borders(Borders::ALL)
                .border_type(border)
                .style(Style::default())
                .blue()
                .bold(),
        )
        .alignment(Alignment::Center),
        centered_rect(60, 100, main_chunks[4]),
    );
    // "PASSWORD CONFIRM"
    let (title, border, switch_title) = {
        if app.mode == Mode::InputPasswordConfirm {
            (Title::from("Typing"), BorderType::Thick, Title::from("Press ↑↓"))
        } else {
            (Title::from(""), BorderType::Plain, Title::from(""))
        }
    };
    f.render_widget(
        Paragraph::new(
            std::iter::repeat('*')
                .take(app.input_buffer.password_confirm.len())
                .collect::<String>()
                .black()
                .bold(),
        )
        .block(
            Block::default()
                .title(Title::from("PASSWORD CONFIRM").alignment(Alignment::Left))
                .title(title.alignment(Alignment::Center))
                .title(switch_title.alignment(Alignment::Right))
                .borders(Borders::ALL)
                .border_type(border)
                .style(Style::default())
                .blue()
                .bold(),
        )
        .alignment(Alignment::Center),
        centered_rect(60, 100, main_chunks[5]),
    );
    // register button
    let (title, bg_color) = {
        if app.mode == Mode::RegisterButton {
            (Title::from("Press ↵"), Color::Rgb(255, 255, 153))
        } else {
            (Title::from(""), Color::Gray)
        }
    };
    f.render_widget(
        Paragraph::new("LOGIN".blue().bold())
            .block(
                Block::default()
                    .title(title.alignment(Alignment::Right))
                    .borders(Borders::NONE)
                    .border_type(border)
                    .style(Style::default())
                    .blue()
                    .bold()
                    .bg(bg_color),
            )
            .alignment(Alignment::Center),
        centered_rect(20, 100, main_chunks[7]),
    );
    // bottom bar
    f.render_widget(
        Paragraph::new(app.notice.clone().green().bold())
            .block(
                Block::default()
                    .title(Title::from("New User".yellow()))
                    .title(Title::from("Status Bar".blue()).alignment(Alignment::Center))
                    .title(Title::from("Switch by Arrows ↑↓".green()).alignment(Alignment::Right))
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
