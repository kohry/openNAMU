from .tool.func import *

def edit_delete_2(conn, name, app_var):
    curs = conn.cursor()

    ip = ip_check()
    if acl_check(name) == 1:
        return re_error('/ban')

    if flask.request.method == 'POST':
        if captcha_post(flask.request.form.get('g-recaptcha-response', '')) == 1:
            return re_error('/error/13')
        else:
            captcha_post('', 0)

        if slow_edit_check() == 1:
            return re_error('/error/24')

        curs.execute(db_change("select data from data where title = ?"), [name])
        data = curs.fetchall()
        if data:
            today = get_time()
            leng = '-' + str(len(data[0][0]))

            history_plus(
                name,
                '',
                today,
                ip,
                flask.request.form.get('send', ''),
                leng,
                'delete'
            )

            curs.execute(db_change("select title, link from back where title = ? and not type = 'cat' and not type = 'no'"), [name])
            for data in curs.fetchall():
                curs.execute(db_change("insert into back (title, link, type) values (?, ?, 'no')"), [data[0], data[1]])

            curs.execute(db_change("delete from back where link = ?"), [name])
            curs.execute(db_change("delete from data where title = ?"), [name])
            conn.commit()

        file_check = re.search('^file:(.+)\.(.+)$', name)
        if file_check:
            file_check = file_check.groups()
            os.remove(os.path.join(
                app_var['path_data_image'],
                sha224_replace(file_check[0], 'utf-8') + '.' + file_check[1]
            ))

        curs.execute(db_change('select data from other where name = "count_all_title"'))
        curs.execute(db_change("update other set data = ? where name = 'count_all_title'"), [str(int(curs.fetchall()[0][0]) - 1)])

        return redirect('/w/' + url_pas(name))
    else:
        curs.execute(db_change("select title from data where title = ?"), [name])
        if not curs.fetchall():
            return redirect('/w/' + url_pas(name))

        return easy_minify(flask.render_template(skin_check(),
            imp = [name, wiki_set(), custom(), other2([' (' + load_lang('delete') + ')', 0])],
            data =  '''
                    <form method="post">
                        ''' + ip_warring() + '''
                        <input placeholder="''' + load_lang('why') + '''" name="send" type="text">
                        <hr class=\"main_hr\">
                        ''' + captcha_get() + '''
                        <button type="submit">''' + load_lang('delete') + '''</button>
                    </form>
                    ''',
            menu = [['w/' + url_pas(name), load_lang('return')]]
        ))     