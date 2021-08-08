#include <gtk/gtk.h>
#include <glib/gstdio.h>

#include <stdio.h>
#include <stdlib.h>

#include <errno.h>
#include <fcntl.h>

#include "machyapi.h"

static void
send_test000001 (GtkWidget *widget,
             gpointer   data)
{
  printf("send: TEST000001\n");
  machy_request("TEST000001");
}

static void
send_echo000001 (GtkWidget *widget,
              gpointer data)
{
  printf("send: ECHO000001");
  machy_request("ECHO000001");
}

static void
send_trajsim001 (GtkWidget *widget,
              gpointer data)
{
  char *message = "TRAJSIM001:";
  char *file_contents = read_file("trajectory_1.txt");
  char buf[strlen(message)+strlen(file_contents)];
  strcat(strcpy(buf, message), file_contents);
  machy_request(buf);
}

static void
send_start00001 (GtkWidget *widget,
              gpointer data)
{
  machy_request("START00001");
}

static void
hello_world (GtkWidget *widget,
          gpointer data)
{
  printf("hello world!\n");
}

static void
quit_cb (GtkWindow *window)
{
  cleanup();
  gtk_window_close (window);
}

#ifdef FILE_DIALOG
static void
on_open_response(GtkDialog *dialog,
                int response)
{
  if (response == GTK_RESPONSE_ACCEPT)
  {
    GtkFileChooser *chooser = GTK_FILE_CHOOSER (dialog);

    g_autoptr(GFile) file = gtk_file_chooser_get_file_name (chooser);

    gsize length;
    gchar *contents;

    if (g_file_get_contents(&file, &contents, &length, NULL)){
      //fprintf(stderr, "get_contents() failed. (%d)\n", errno);
      printf("read file\n");
      g_strdup_printf("contents : %s\n", contents);
      g_free (contents);
    }
    else
      printf("something wrong!\n");
  }
  gtk_window_destroy (GTK_WINDOW (dialog));
}

static void
send_trajsim001 (GObject *window)
{
  GtkWidget *dialog;
  GtkFileChooserAction action = GTK_FILE_CHOOSER_ACTION_OPEN;
  dialog = gtk_file_chooser_dialog_new ("Open File", window, action, 
                                        ("_Cancel"), GTK_RESPONSE_CANCEL,
                                        ("_Open"), GTK_RESPONSE_ACCEPT, NULL);
  GtkFileFilter *filter = gtk_file_filter_new ();
  gtk_file_filter_add_pattern (filter, "*.txt");
  gtk_file_chooser_set_filter(dialog, filter);
  gtk_widget_show (dialog);
  g_signal_connect (dialog, "response", G_CALLBACK(on_open_response), NULL);
}
#endif

static void
activate (GtkApplication *app,
          gpointer        user_data)
{
  // printf("user data : %s", &user_data);
  /* Construct a GtkBuilder instance and load our UI description */
  GtkBuilder *builder = gtk_builder_new();
  gtk_builder_add_from_file (builder, "src/builder.ui", NULL);

  /* Connect signal handlers to the constructed widgets. */
  GObject *window = gtk_builder_get_object (builder, "window");
  gtk_window_set_application (GTK_WINDOW (window), app);

  GObject *button = gtk_builder_get_object (builder, "TEST1");
  g_signal_connect (button, "clicked", G_CALLBACK (send_test000001), NULL);

  button = gtk_builder_get_object (builder, "ECHO1");
  g_signal_connect (button, "clicked", G_CALLBACK (send_echo000001), NULL);

  button = gtk_builder_get_object (builder, "HELLO");
  g_signal_connect (button, "clicked", G_CALLBACK (hello_world), NULL);

  button = gtk_builder_get_object (builder, "TRAJSIM001");
  g_signal_connect (button, "clicked", G_CALLBACK (send_trajsim001), NULL);

  button = gtk_builder_get_object (builder, "START00001");
  g_signal_connect (button, "clicked", G_CALLBACK (send_start00001), NULL);

  button = gtk_builder_get_object (builder, "quit");
  g_signal_connect_swapped (button, "clicked", G_CALLBACK (quit_cb), window);

  gtk_widget_show (GTK_WIDGET (window));

  /* We do not need the builder any more */
  g_object_unref (builder);
}

int
main (int   argc,
      char *argv[])
{
#ifdef GTK_SRCDIR
  g_chdir (GTK_SRCDIR);
#endif

  GtkApplication *app = gtk_application_new ("org.gtk.example", G_APPLICATION_FLAGS_NONE);
  g_signal_connect (app, "activate", G_CALLBACK (activate), NULL);

  int status = g_application_run (G_APPLICATION (app), argc, argv);
  g_object_unref (app);

  return status;
}