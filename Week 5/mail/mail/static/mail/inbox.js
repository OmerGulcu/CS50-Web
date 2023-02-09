document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', () => compose_email(null));

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email(email) {

  // Show compose view and hide other views
  const emailView = document.querySelector('#email-view');
  emailView.innerHTML = '';
  emailView.style.display = 'none';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  let compose_recipients = document.querySelector('#compose-recipients');
  let compose_subject = document.querySelector('#compose-subject');
  let compose_body = document.querySelector('#compose-body');
  if (!email) {
    // Clear out composition fields
    compose_recipients.value = '';
    compose_recipients.disabled = false;
    compose_recipients.focus();
    compose_subject.value = '';
    compose_subject.disabled = false;
    compose_body.value = '';
  }
  else {
    compose_recipients.value = email.sender;
    compose_recipients.disabled = true;
    if (email.subject.substring(0, 4) !== 'Re: ') {
      compose_subject.value = `Re: ${email.subject}`;
    }
    else {
      compose_subject.value = email.subject;
    }
    compose_subject.disabled = true;
    compose_body.focus();
    if (email.body.indexOf('---Type your reply after this line---') === -1) {
      compose_body.value = `On ${email.timestamp} ${email.sender} wrote:\n${email.body}\n\n---Type your reply after this line---\n`;
    }
    else {
      compose_body.value = `${email.body.replace('---Type your reply after this line---', `On ${email.timestamp} ${email.sender} replied:`)}\n\n---Type your reply after this line---\n`;
    }
    
  }
  
  // Compose form sends the mail
  document.querySelector('#compose-form').onsubmit = () => {
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value,
        subject: document.querySelector('#compose-subject').value,
        body: document.querySelector('#compose-body').value
      })
    })
    .then(response => response.json())
    .then(result => {
      console.log(result);
    })
    .then(() => {
      // Load sent mailbox
      load_mailbox('sent');
    });

    return false;
  }
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  const emailView = document.querySelector('#email-view');
  emailView.innerHTML = '';
  emailView.style.display = 'none';
  const emailsView = document.querySelector('#emails-view');
  emailsView.style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  emailsView.innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    emails.forEach(email => {
      let maildiv = document.createElement('div');
      maildiv.className = 'email';
      maildiv.id = `mail no ${email.id}`;
      maildiv.innerHTML = `<span class="preview_left"><b>${email.sender} </b>&nbsp&nbsp${email.subject}</span><span class="preview_right"><span class="timestamp">${email.timestamp} &nbsp&nbsp</span><img class="preview_image" id="archive no ${email.id}" src="http://127.0.0.1:8000/static/mail/download-button.png"></span>`;
      if (email.read === true) {
        maildiv.style.backgroundColor = 'lightgrey';
      }
      emailsView.append(maildiv);
    })
  })
  .then(() => { // Anchor the previews to the mail view
    document.querySelectorAll('.preview_image').forEach(image => {
      image.onclick = (event) => {
        toggle_archive(image.id.substring(11))
        event.stopPropagation();
      }
    })
    document.querySelectorAll('.email').forEach(div => {
      div.onclick = () => {
        view_email(div.id.substring(8));
      }
    });
  });
}

function view_email(id) {
  const emailView = document.querySelector('#email-view');
  const emailsView = document.querySelector('#emails-view');

  emailsView.style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  emailView.style.display = 'block';

  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
    let body = '';
    for (let i = 0; i < email.body.length; i++) {
      if (email.body.charAt(i) === '\n') {
        body += '<br>'
      }
      else {
        body += email.body.charAt(i);
      }
    }
    let archiveLabel;
    if (email.archived) {
      archiveLabel = "Unarchive";
    }
    else {
      archiveLabel = "Archive";
    }
    emailView.innerHTML = `From: <b>${email.sender}</b><br>To: <b>${email.recipients.join(', ')}</b><br><br><h4>${email.subject}</h4><p class="timestamp">${email.timestamp}</p>${body}
    <br><br><br><br>Reply &nbsp&nbsp&nbsp<img class="view_mail_image" id="reply_image" src="http://127.0.0.1:8000/static/mail/reply.png"><br>${archiveLabel} <img class="view_mail_image" id="archive_image" src="http://127.0.0.1:8000/static/mail/download-button.png">`;
    fetch(`/emails/${email.id}`, {
      method: 'PUT',
      body: JSON.stringify({
        read: true
      })
    });
    return email;
  })
  .then(email => {
    document.querySelector('#archive_image').addEventListener('click', () => {
      toggle_archive(email.id);
    });
    document.querySelector('#reply_image').addEventListener('click', () => {
      compose_email(email);
    });
  });
}

function toggle_archive(id) {
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
    fetch(`/emails/${id}`, {
      method: 'PUT',
      body: JSON.stringify({
        archived: !email.archived
      })
    })
    .then(() => {
      load_mailbox('inbox');
    });
  });
}