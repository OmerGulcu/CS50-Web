document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

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
    });

    // Load sent mailbox
    load_mailbox('sent');
    return false;
  }

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  const emailView = document.querySelector('#email-view');
  emailView.innerHTML = '';
  emailView.style.display = 'none';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
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
    console.log(emails);
    emails.forEach(email => {
      console.log(email);
      let maildiv = document.createElement('div');
      maildiv.className = 'email';
      maildiv.id = `mail no ${email.id}`;
      maildiv.innerHTML = `<p>From: <b>${email.sender}</b><br>Subject: ${email.subject}</p><p class="timestamp">${email.timestamp}</p>`;
      if (email.read === true) {
        maildiv.style.backgroundColor = 'lightgrey';
      }
      emailsView.append(maildiv);
    })
  })
  .then(() => { // Anchor the previews to the mail view
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
    emailView.innerHTML = `From: <b>${email.sender}</b><br>To: <b>${email.recipients.join(', ')}</b><br><br><h4>${email.subject}</h4><p class="timestamp">${email.timestamp}</p>${body}`;
    fetch(`/emails/${email.id}`, {
      method: 'PUT',
      body: JSON.stringify({
        read: true
      })
    });
  });
}