# NoteJAM API Documentation

NoteJAM API is a project connected to the NoteJAM app.

# Sections

## [REGISTRATION]() [LESSONS]() [NOTES]() [STUDIO]() [PROFILES]() [PRACTICE]() [DOCUMENTS]()

## Headers

Requests to endpoints requiring authentication should set the Authorization header to **Token <token>**, where **<token>** is the token received in the login response.

POST requests with a body should set the **Content-Type** header to **application/json**

---

# REGISTRATION | LOGIN | LOGOUT

---

## Register an Instructor

https://music-mvp.herokuapp.com/auth/users/

### request

'first_name', 'last_name', 'email', 'phone', 'emergency_contact_name', 'emergency_contact_phone' are required fields.

is_instructor defaults as True without having to be passed at this endpoint

```jsx
POST auth/users/

{
	"first_name": "Sami",
    "last_name": "S",
    "email": "samuli_roche@email.com",
    "username": "samuli_5",
	"password": "somepassword",
	"re_password": "somepassword",
	"emergency_contact_phone": "5555555555",
	"emergency_contact_name": "Mom"
}
```

### response

```jsx
201 Created

{
  "first_name": "Sami",
  "last_name": "S",
  "email": "samuli_roche@email.com",
  "phone": "",
  "instructor": null,
  "is_instructor": true,
  "emergency_contact_name": "Mom",
  "emergency_contact_phone": "5555555555",
  "username": "samuli_5",
  "id": 25
}
```

## Register a Student

https://music-mvp.herokuapp.com/api/users/students/pk/

### request

'instructor', 'first_name', 'last_name', 'email', 'phone', 'emergency_contact_name', 'emergency_contact_phone' are required fields.

'instructor' field must be passed through as pk in the URL.

is_instructor defaults as False without having to be passed at this endpoint

```jsx
POST api/users/students/11/

{
	"first_name": "Asya",
    "last_name": "Tumelo",
    "email": "asya@email.com",
    "username": "cello",
	"phone": "555555555",
	"password": "somepassword",
	"re_password": "somepassword",
	"emergency_contact_phone": "5555555555",
	"emergency_contact_name": "Baba",
}
```

### response

```jsx
201 Created

{
  "is_instructor": false,
  "instructor": 11,
  "first_name": "Asya",
  "last_name": "Tumelo",
  "username": "cello",
  "email": "asya@email.com",
  "phone": "555555555",
  "emergency_contact_name": "Baba",
  "emergency_contact_phone": "5555555555"
}
```

## Sending Student a Registration Invite Email

https://music-mvp.herokuapp.com/api/mail/send/

### request

'instructor_url' in request must contain instructor's pk

```jsx
POST /
  api /
  mail /
  send /
  {
    name: "Kayla",
    email: "Kayla123@email.com",
    instructor_url: "https://your-url-to-register-students.com/",
  };
```

### response

```jsx
200 OK

{
  "success": "Sent"
}
```

## Login

https://music-mvp.herokuapp.com/auth/token/login/

### request

```jsx
POST auth/token/login/

{
"username": "seagull",
"password": "somepassword"
}
```

### response

```jsx
200 OK

{
  "auth_token": "d60e585cc8383003742831e7937e1969b3bbbed3"
}
```

## Logout

https://music-mvp.herokuapp.com/auth/token/logout/

### request

Requires authentication.

```jsx
POST auth/token/logout/
```

### response

```jsx
HTTP_204_NO_CONTENT;
```

---

# LESSONS

---

## List of Upcoming Instructor Lessons for the Day

https://music-mvp.herokuapp.com/api/upcoming/

### request

Requires authentication.

Must be **instructor user**.

```jsx
GET api/upcoming/
```

### response

```jsx
200 OK

[
  {
    "pk": 54,
    "student": 4,
    "student_name": "Oscar Ostrich",
    "lesson_date": "Oct. 12, 2021",
    "lesson_time": "5:06PM"
  },
  {
    "pk": 53,
    "student": 11,
    "student_name": "Baldine Eaglie",
    "lesson_date": "Oct. 12, 2021",
    "lesson_time": "6:05PM"
  }
]
```

## List of Upcoming and Past Student Lessons

https://music-mvp.herokuapp.com/api/upcoming/

### request

Requires authentication.

Must be **student user.**

```jsx
GET api/upcoming/
```

### response

```jsx
200 OK

[
  {
    "pk": 67,
    "student": 3,
    "lesson_date": "Oct. 11, 2021",
    "lesson_time": "9:30AM",
    "note": [
      {
        "pk": 45,
        "body": "practice!",
        "lesson": 67,
        "is_assignment": false,
        "created_at": "Oct. 11, 2021 at 9:02AM"
      }
    ]
  },
  {
    "pk": 1,
    "student": 3,
    "lesson_date": "Oct. 06, 2021",
    "lesson_time": "6:09PM",
    "note": []
  },
  {
    "pk": 2,
    "student": 3,
    "lesson_date": "Oct. 05, 2021",
    "lesson_time": "6:09PM",
    "note": [
      {
        "pk": 41,
        "body": "Make sure to bring your music!",
        "lesson": 2,
        "is_assignment": true,
        "created_at": "Oct. 10, 2021 at 10:59AM"
      }
    ]
  }
]
```

## List of Students Upcoming and Past Lessons (viewable by instructor)

https://music-mvp.herokuapp.com/api/assignments/student_pk/

### request

Requires authentication. Must pass through user pk of student

```jsx
GET api/assignments/2/
```

### response

```jsx
200 OK

[
  {
    "pk": 6,
    "student": 2,
    "lesson_date": "Oct. 11, 2021",
    "lesson_time": "6:09PM",
    "note": [
      {
        "pk": 48,
        "body": "practice!",
        "lesson": 6,
        "is_assignment": false,
        "created_at": "Oct. 11, 2021 at 9:02AM"
      }
    ]
  },
  {
    "pk": 69,
    "student": 2,
    "lesson_date": "Oct. 11, 2021",
    "lesson_time": "1:00PM",
    "note": [
      {
        "pk": 47,
        "body": "practice!",
        "lesson": 69,
        "is_assignment": false,
        "created_at": "Oct. 11, 2021 at 9:02AM"
      }
    ]
  },
  {
    "pk": 72,
    "student": 2,
    "lesson_date": "Oct. 11, 2021",
    "lesson_time": "10:30AM",
    "note": []
  },
  {
    "pk": 71,
    "student": 2,
    "lesson_date": "Oct. 11, 2021",
    "lesson_time": "2:06AM",
    "note": [
      {
        "pk": 50,
        "body": "1. practice\n2. practice more\n3. practice something else\n4. keep practicing.",
        "lesson": 71,
        "is_assignment": true,
        "created_at": "Oct. 11, 2021 at 2:07PM"
      }
    ]
  }
]
```

## List of Previous Lesson Plans and Assignments for a Student

https://music-mvp.herokuapp.com/api/assignments/student_pk/previous/pk

### request

Requires authentication.

Must pass through user pk of student in student_pk and lesson pk in pk.

There may still be out

Only return last 5 lessons that are older than the date on lesson in the pk.

```jsx
GET api/assignments/2/previous/69/
```

### response

```jsx
200 OK

[
  {
    "pk": 6,
    "lesson_date": "Oct. 11, 2021",
    "lesson_time": "6:09PM",
    "plan": null,
    "student": 2,
    "student_name": "Greta Goose",
    "author": "admin",
    "created_at": "Oct. 05, 2021 at 1:49PM",
    "note": [
      {
        "pk": 48,
        "body": "practice!",
        "lesson": 6,
        "is_assignment": false,
        "created_at": "Oct. 11, 2021 at 9:02AM"
      }
    ]
  },
  {
    "pk": 69,
    "lesson_date": "Oct. 11, 2021",
    "lesson_time": "1:00PM",
    "plan": "teach studen",
    "student": 2,
    "student_name": "Greta Goose",
    "author": "baldeagle",
    "created_at": "Oct. 11, 2021 at 8:35AM",
    "note": [
      {
        "pk": 47,
        "body": "practice!",
        "lesson": 69,
        "is_assignment": false,
        "created_at": "Oct. 11, 2021 at 9:02AM"
      }
    ]
  },
  {
    "pk": 66,
    "lesson_date": "Oct. 11, 2021",
    "lesson_time": "8:30AM",
    "plan": "1. teach something.\n2. teach something else\n3. teach another thing.",
    "student": 2,
    "student_name": "Greta Goose",
    "author": "baldeagle",
    "created_at": "Oct. 11, 2021 at 8:34AM",
    "note": [
      {
        "pk": 43,
        "body": "practice breathing",
        "lesson": 66,
        "is_assignment": true,
        "created_at": "Oct. 11, 2021 at 8:36AM"
      },
      {
        "pk": 44,
        "body": "practice!",
        "lesson": 66,
        "is_assignment": false,
        "created_at": "Oct. 11, 2021 at 9:02AM"
      }
    ]
  },
  {
    "pk": 65,
    "lesson_date": "Oct. 10, 2021",
    "lesson_time": "8:59AM",
    "plan": "teach",
    "student": 2,
    "student_name": "Greta Goose",
    "author": "baldeagle",
    "created_at": "Oct. 10, 2021 at 8:00PM",
    "note": []
  }
]
```

## Add a Lesson

https://music-mvp.herokuapp.com/api/lessons/

### request

Requires authentication.

**lesson_date** and **lesson_time** are required fields.

Plan can be null when the lesson is created and updated later.

Author field is automatically populated based on authenticated user

```jsx
POST api/lessons/

{
	"student": 2,
	"lesson_date": "2021-10-11",
	"lesson_time": "10:30"
}
```

### response

```jsx
201 Created

{
  "id": 73,
  "lesson_date": "Oct. 11, 2021",
  "lesson_time": "10:30AM",
  "author": "baldeagle",
  "created_at": "Oct. 12, 2021 at 4:04PM",
  "plan": null,
  "student": 2
}
```

## View Lesson Detail

https://music-mvp.herokuapp.com/api/lessons/pk/

### request

Requires authentication. Must be owner of the lesson.

```jsx
GET api/lessons/1/
```

### response

```jsx
200 OK

{
  "pk": 1,
  "lesson_date": "Oct. 06, 2021",
  "lesson_time": "6:09PM",
  "plan": "New text here for update, with more updates_more stuff, look it work.... still? YUP plzzzz",
  "student": "Sam Seagull",
  "author": "goose",
  "created_at": "Oct. 05, 2021 at 10:02AM",
  "note": []
}
```

## Update Lesson

https://music-mvp.herokuapp.com/api/lessons/pk/

### request

Requires authentication. Must be owner of the lesson. Can be a **PATCH** or **PUT**.

lesson_date, lesson_time are required fields.

```jsx
PATCH api/lessons/10/

{
	"lesson_date": "2021-10-06",
	"plan": "New text here for update, with more updates_more stuff, look it work.... still? YUP plzzzz... heck yea!",
    "student": "goose",
    "author": "zelda"
}
```

### response

```jsx
200 OK

{
  "pk": 1,
  "lesson_date": "Oct. 06, 2021",
  "lesson_time": "6:09PM",
  "plan": "New text here for update, with more updates_more stuff, look it work.... still? YUP plzzzz... heck yea!",
  "student": "Sam Seagull",
  "author": "goose",
  "created_at": "Oct. 05, 2021 at 10:02AM",
  "note": []
}
```

## Delete Lesson

https://music-mvp.herokuapp.com/api/lessons/pk/

### request

Requires authentication. Must be owner of the lesson.

```jsx
DEL api/lessons/1/
```

### response

```jsx
204 Not Content
```

---

# NOTES

---

## Add a Note

https://music-mvp.herokuapp.com/api/note/

### request

Requires authentication. Must give it lesson as a pk.

Author field is automatically populated based on authenticated user

```jsx
POST api/note/

{
  "body": "goose goose goose goose",
  "lesson": 1,
  "is_assignment": true
}
```

### response

```jsx
200 OK

{
  "pk": 57,
  "body": "goose goose goose goose",
  "lesson": 1,
  "is_assignment": true,
  "created_at": "Oct. 12, 2021 at 04:07 PM"
}
```

## List Notes

https://music-mvp.herokuapp.com/api/note/

### request

Requires authentication. Must be owner of notes.

```jsx
GET api/note/
```

### response

```jsx
200 OK

[
  {
    "pk": 3,
    "body": "Hewwo (this is an assignment)",
    "lesson": 3,
    "is_assignment": true,
    "created_at": "Oct. 06, 2021 at 08:24 AM"
  },
  {
    "pk": 35,
    "body": "F# major scale\nDvorak 2nd mvmt",
    "lesson": 16,
    "is_assignment": true,
    "created_at": "Oct. 07, 2021 at 09:46 PM"
  },
  {
    "pk": 57,
    "body": "goose goose goose goose",
    "lesson": 1,
    "is_assignment": true,
    "created_at": "Oct. 12, 2021 at 04:07 PM"
  }
]
```

## Note Details

https://music-mvp.herokuapp.com/api/note/pk/

### request

Requires authentication. Must be owner of note.

```jsx
GET api/note/53/
```

### response

```jsx
200 OK

{
  "pk": 53,
  "body": "practice more",
  "lesson": 74,
  "is_assignment": true,
  "created_at": "Oct. 11, 2021 at 08:33 PM"
}
```

## Update Note

https://music-mvp.herokuapp.com/api/note/pk/

### request

Requires authentication. Must be owner of note.

```jsx
PUT api/note/53/

{
  "body": "goose goose",
  "lesson": 1,
  "is_assignment": true
}
```

### response

```jsx
200 OK

{
  "pk": 53,
  "body": "goose goose",
  "lesson": 1,
  "is_assignment": true,
  "created_at": "Oct. 11, 2021 at 08:33 PM"
}

```

## Delete Note

https://music-mvp.herokuapp.com/api/note/pk/

### request

Requires authentication. Must be owner of note.

```jsx
DELETE api/note/1/
```

### response

```jsx
204 Not Content
```

---

# PROFILES

---

## Users View of their Profile

https://music-mvp.herokuapp.com/auth/users/me/

### request

Requires authentication.

```jsx
GET auth/users/me/
```

### response

```jsx
200 OK

{
  "first_name": "Sam",
  "last_name": "Seagull",
  "email": "seagull@email.com",
  "phone": "1234567891",
  "instructor": null,
  "is_instructor": false,
  "emergency_contact_name": "Baba",
  "emergency_contact_phone": "5555555555",
  "id": 3,
  "username": "seagull"
}
```

## Edit Your Profile

https://music-mvp.herokuapp.com/auth/users/me/

### request

Requires authentication. All user types.

```jsx
PATCH auth/users/me/

{
  "email": "seayall@email.com"
}
```

### response

```jsx
200 OK

{
  "first_name": "Sam",
  "last_name": "Seagull",
  "email": "seayall@email.com",
  "phone": "1234567891",
  "instructor": 11,
  "is_instructor": false,
  "emergency_contact_name": "Baba",
  "emergency_contact_phone": "5555555555",
  "id": 3,
  "username": "seagull"
}
```

## Delete Your Profile

https://music-mvp.herokuapp.com/auth/users/me/

### request

Requires authentication. current_password is required.

All user types can delete their own user profile. **_(We can add a way to delete a student by an instructor at some point if yall want)_**

```jsx
DELETE auth/users/me/

{
  "current_password": "somepassword"
}
```

### response

```jsx
204 NO CONTENT
```

## Instructor View for Individual Student Profile

https://music-mvp.herokuapp.com/api/users/pk/

### request

Requires authentication. Must have student.

```jsx
GET api/users/14/
```

### response

```jsx
200 OK

{
  "pk": 14,
  "first_name": "test",
  "last_name": "fordata",
  "username": "tfd",
  "email": "e@mail.com",
  "phone": "5555555555",
  "instructor": 11,
  "emergency_contact_name": "Baba",
  "emergency_contact_phone": "5555555555"
}
```

---

# STUDIO

---

## Instructor's Studio

https://music-mvp.herokuapp.com/instructor/studio/

List of logged in instructor's active students in studio

### request

Requires authentication. Must have student.

```jsx
GET [instructor/studio/](http://127.0.0.1:8000/instructor/studio/)
```

### response

```jsx
200 OK

[
  {
    "pk": 2,
    "first_name": "Greta",
    "last_name": "Goose",
    "username": "goose",
    "email": "goose@honk.com",
    "phone": "",
    "created_at": "Oct. 16, 2021"
  },
  {
    "pk": 24,
    "first_name": "Sami",
    "last_name": "S",
    "username": "samuli_s",
    "email": "samuli_roche@email.com",
    "phone": "",
    "created_at": "Oct. 16, 2021"
  },
  {
    "pk": 23,
    "first_name": "Samuli",
    "last_name": "S",
    "username": "samuli",
    "email": "samuli_roche@email.com",
    "phone": "",
    "created_at": "Oct. 16, 2021"
  },
  {
    "pk": 17,
    "first_name": "LittleDuck",
    "last_name": "aaa",
    "username": "LittleDuck",
    "email": "aaa@gmail.com",
    "phone": "1111111111",
    "created_at": "Oct. 16, 2021"
  }
]
```

## Search in Studio

https://music-mvp.herokuapp.com/instructor/studio/?search={search term}

### request

Requires authentication.

Must be an instructor.

Search by first name, last name and username. Does not have to be an exact match.

```jsx
GET [instructor/studio/](http://127.0.0.1:8000/instructor/studio/)?search=sam
```

### response

```jsx
200 OK

[
  {
    "pk": 23,
    "first_name": "Samuli",
    "last_name": "S",
    "username": "samuli",
    "email": "samuli_roche@email.com",
    "phone": "",
    "created_at": "Oct. 16, 2021"
  },
  {
    "pk": 24,
    "first_name": "Sami",
    "last_name": "S",
    "username": "samuli_s",
    "email": "samuli_roche@email.com",
    "phone": "",
    "created_at": "Oct. 16, 2021"
  }
]
```

## Marking Student as Active or Inactive in Studio

https://music-mvp.herokuapp.com/instructor/studio/pk/

Will remove inactive students from studio list.

### request

Requires authentication. Must pass **pk of student user** through URL.

```jsx
PATCH [instructor/studio/](http://127.0.0.1:8000/instructor/studio/)5/

{
	"active_in_studio": false
}
```

### response

```jsx
200 OK

{
  "pk": 5,
  "first_name": "a",
  "last_name": "v",
  "username": "av",
  "email": "",
  "phone": "",
  "instructor": 11,
  "active_in_studio": false,
  "emergency_contact_name": "unknown",
  "emergency_contact_phone": "5555555555"
}
```

---

# PRACTICE LOGS

---

## List Practice Logs

https://music-mvp.herokuapp.com/api/practices/

### request

Requires authentication. Returns the practice logs for the authenticated user.

```jsx
GET api/practices/
```

### response

```jsx
200 OK

[
  {
    "pk": 4,
    "time_practiced": 3,
    "body": "so much practice",
    "created_at": "Oct. 11, 2021 at 6:36PM",
    "author": "seagull"
  },
  {
    "pk": 3,
    "time_practiced": 5,
    "body": "practice",
    "created_at": "Oct. 11, 2021 at 6:09PM",
    "author": "seagull"
  },
  {
    "pk": 2,
    "time_practiced": 10,
    "body": "all the music",
    "created_at": "Oct. 11, 2021 at 6:08PM",
    "author": "seagull"
  },
  {
    "pk": 1,
    "time_practiced": 20,
    "body": "lots of things",
    "created_at": "Oct. 11, 2021 at 6:05PM",
    "author": "seagull"
  }
]
```

## Add Practice Logs

https://music-mvp.herokuapp.com/api/practices/

### request

Requires authentication.

Author field is automatically populated based on authenticated user

```jsx
POST api/practices/

{
"body": "so much practice",
"time_practiced": "3"
}
```

### response

```jsx
201 Created

{
  "pk": 5,
  "time_practiced": 3,
  "body": "so much practice",
  "created_at": "Oct. 12, 2021 at 4:19PM",
  "author": "seagull"
}
```

## Delete Practice Logs

https://music-mvp.herokuapp.com/api/practices/pk/

### request

Requires authentication.

```jsx
DELETE api/practices/5/
```

### response

```jsx
204 No Content
```

## Updating Practice Logs

https://music-mvp.herokuapp.com/api/practices/pk/

### request

Requires authentication.

```jsx
PATCH api/practices/5/

{
"body": "so much UPDATED practice",
"time_practiced": "3"
}
```

### response

```jsx
201 OK

{
  "pk": 5,
  "time_practiced": 3,
  "body": "so much UPDATED practice",
  "created_at": "Oct. 12, 2021 at 4:19PM",
  "author": "seagull"
}
```

---

# DOCUMENTS

---

## Create Documents

This endpoint takes two requests to create the document object and upload the file.

https://music-mvp.herokuapp.com/api/documents/

### request

Requires authentication. Title field is required. Attaches author as authenticated user.

```jsx
POST api/documents/

{
	"title": "Let's Go",
}
```

### response

```jsx
201 Created

{
  "pk": 15,
  "uploaded_at": "Oct. 18, 2021 at 10:31AM",
  "title": "Lets Go!",
  "upload": null,
  "author": "baldeagle",
  "students": [],
  "tags": []
}
```

### **Now to add the file with a second request:**

https://music-mvp.herokuapp.com/api/documents/pk/upload/

**There are different request settings for this endpoint.**

For the request file, you will need to set it to a **binary file** and **attach the file** to the request.

Next you will need to change your request headers to be:
**Content-Type** set to **application/{file.type} (ex: application/pdf)**
**Content-Disposition** set to **attachment; filename={somefilename.pdf}**

### request

Requires authentication.

```jsx
PUT api/documents/5/upload/

select binary file
```

![Screen Shot 2021-10-14 at 8.59.50 AM.png](HONK%20API%20Documentation%205143179b171342bd83be89d2e64cea23/Screen_Shot_2021-10-14_at_8.59.50_AM.png)

### response

```jsx
201 Created
```

## List Documents for Instructor or Student

https://music-mvp.herokuapp.com/api/documents/

### request

Requires authentication.

```jsx
GET api/documents/
```

### response for Instructor

```jsx
200 OK

[

  {
    "pk": 11,
    "uploaded_at": "Oct. 15, 2021 at 10:11AM",
    "title": "A File",
    "upload": "https://screamteam-static.s3.amazonaws.com/media/somekindofimage.png",
    "author": "baldeagle",
    "students": [],
    "tags": []
  },
  {
    "pk": 10,
    "uploaded_at": "Oct. 14, 2021 at 1:30PM",
    "title": "A File",
    "upload": "https://screamteam-static.s3.amazonaws.com/media/somekindofimage.png",
    "author": "baldeagle",
    "students": [],
    "tags": []
  },
  {
    "pk": 9,
    "uploaded_at": "Oct. 14, 2021 at 10:52AM",
    "title": "A File",
    "upload": "https://screamteam-static.s3.amazonaws.com/media/somekindofimage.pdf",
    "author": "baldeagle",
    "students": [],
    "tags": []
  },
  {
    "pk": 4,
    "uploaded_at": "Oct. 14, 2021 at 8:49AM",
    "title": "A File",
    "upload": "https://screamteam-static.s3.amazonaws.com/media/somekindofpdf.pdf",
    "author": "baldeagle",
    "students": [],
    "tags": []
  },
  {
    "pk": 3,
    "uploaded_at": "Oct. 14, 2021 at 8:49AM",
    "title": "A File",
    "upload": "https://screamteam-static.s3.amazonaws.com/media/somekindofpdf.pdf",
    "author": "baldeagle",
    "students": [
      "admin",
      "baldeagle",
      "oscar",
      "seagull",
      "opheliacello",
      "goose2"
    ],
    "tags": [
      "10/18/2021",
      "notes"
    ]
  },
  {
    "pk": 2,
    "uploaded_at": "Oct. 13, 2021 at 10:12PM",
    "title": "This is a File",
    "upload": "https://screamteam-static.s3.amazonaws.com/media/somekindofpdf.pdf",
    "author": "baldeagle",
    "students": [
      "av"
    ],
    "tags": []
  },
  {
    "pk": 1,
    "uploaded_at": "Oct. 13, 2021 at 8:26PM",
    "title": "This is a File",
    "upload": "https://screamteam-static.s3.amazonaws.com/media/somekindofpdf.pdf",
    "author": "baldeagle",
    "students": [],
    "tags": []
  }
]
```

### response for Student (goose2)

```jsx
200 OK

[
  {
    "pk": 14,
    "uploaded_at": "Oct. 17, 2021 at 4:37PM",
    "title": "Search happy",
    "upload": null,
    "author": "baldeagle",
    "students": [
      "goose2"
    ],
    "tags": []
  },
  {
    "pk": 3,
    "uploaded_at": "Oct. 14, 2021 at 8:49AM",
    "title": "A File",
    "upload": null,
    "author": "baldeagle",
    "students": [
      "admin",
      "baldeagle",
      "oscar",
      "seagull",
      "opheliacello",
      "goose2"
    ],
    "tags": [
      "10/18/2021",
      "notes"
    ]
  }
]
```

## View Document Details

https://music-mvp.herokuapp.com/api/documents/pk/

### request

Requires authentication.

```jsx
GET api/documents/3/
```

### response

```jsx
200 OK

{
  "pk": 3,
  "uploaded_at": "Oct. 14, 2021 at 8:49AM",
  "title": "A File",
  "upload": null,
  "author": "baldeagle",
  "students": [
    "admin",
    "baldeagle",
    "oscar",
    "seagull",
    "opheliacello",
    "goose2"
  ],
  "tags": [
    "10/18/2021",
    "notes"
  ]
}
```

## Add Students and Tags to Document

https://music-mvp.herokuapp.com/api/documents/pk/

### request

Requires authentication. Add student pk and/or tag pk to the array of students already listed. Might need to do a GET request first.

```jsx
PATCH api/documents/3/

{
	"students": [11, 9, 10, 9, 1, 3, 4],
	"tags": [7, 10, 12]
}
```

### response

```jsx
200 OK

{
  "pk": 3,
  "uploaded_at": "Oct. 14, 2021 at 8:49AM",
  "title": "A File",
  "upload": null,
  "author": "baldeagle",
  "students": [
    "admin",
    "baldeagle",
    "oscar",
    "seagull",
    "opheliacello",
    "goose2"
  ],
  "tags": [
    "10/18/2021",
    "notes",
    "sheet-music"
  ]
}
```

## Delete Document

https://music-mvp.herokuapp.com/api/documents/pk/

### request

Requires authentication.

```jsx
DELETE api/documents/6/
```

### response

```jsx
204 NO CONTENT
```

## Document Search

https://music-mvp.herokuapp.com/api/documents/?search={search term}/

### request

Requires authentication.

Search by title, students and tags. Does not have to be an exact match.

```jsx
GET api/documents/?search=file
```

### response

```jsx
200 OK

[
  {
    "pk": 11,
    "uploaded_at": "Oct. 15, 2021 at 10:11AM",
    "title": "A File",
    "upload": "https://screamteam-static.s3.amazonaws.com/media/somekindofpdf.pdf",
    "author": "baldeagle",
    "students": [],
    "tags": []
  },
  {
    "pk": 10,
    "uploaded_at": "Oct. 14, 2021 at 1:30PM",
    "title": "A File",
    "upload": "https://screamteam-static.s3.amazonaws.com/media/somekindofpdf.pdf",
    "author": "baldeagle",
    "students": [],
    "tags": []
  },
  {
    "pk": 9,
    "uploaded_at": "Oct. 14, 2021 at 10:52AM",
    "title": "A File",
    "upload": "https://screamteam-static.s3.amazonaws.com/media/somekindofpdf.pdf",
    "author": "baldeagle",
    "students": [],
    "tags": []
  },

  {
    "pk": 4,
    "uploaded_at": "Oct. 14, 2021 at 8:49AM",
    "title": "A File",
    "upload": "https://screamteam-static.s3.amazonaws.com/media/somekindofpdf.pdf",
    "author": "baldeagle",
    "students": [],
    "tags": []
  },
  {
    "pk": 2,
    "uploaded_at": "Oct. 13, 2021 at 10:12PM",
    "title": "This is a File",
    "upload": "https://screamteam-static.s3.amazonaws.com/media/somekindofpdf.pdf",
    "author": "baldeagle",
    "students": [
      "av"
    ],
    "tags": []
  },
  {
    "pk": 1,
    "uploaded_at": "Oct. 13, 2021 at 8:26PM",
    "title": "This is a File",
    "upload": "https://screamteam-static.s3.amazonaws.com/media/somekindofpdf.pdf",
    "author": "baldeagle",
    "students": [],
    "tags": []
  }
]
```
