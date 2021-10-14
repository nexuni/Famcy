import os
import json
import urllib
import Famcy
from flask import Flask, g, render_template, redirect, url_for, session, flash, request, Blueprint, current_app, render_template_string, Response

cus = Blueprint('cus', __name__)